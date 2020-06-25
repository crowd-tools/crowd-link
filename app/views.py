import json
import requests

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from web3 import Web3

from . import models, forms, contract


w3 = Web3(Web3.HTTPProvider(settings.INFURA_ROPSTEN_ENDPOINT))
contract_spec = json.loads(contract.abi)
contract_abi = contract_spec["abi"]
contract_instance = w3.eth.contract(abi=contract_abi, address=settings.CONTRACT_INSTANCE_ADDRESS)


class IndexView(generic.TemplateView):
    template_name = 'app/index.html'


class LinkListView(generic.ListView):
    template_name = 'app/link_list.html'
    context_object_name = 'link_list'
    queryset = models.SaleLink.objects.all()


class LinkDetailView(generic.DetailView):
    template_name = 'app/link_detail.html'
    context_object_name = 'link_detail'
    queryset = models.SaleLink.objects.all()


class CampaignListView(generic.ListView):
    template_name = 'app/campaign_list.html'
    context_object_name = 'campaign_list'
    queryset = models.SaleCampaign.objects.all()


class CampaignDetailView(generic.DetailView):
    template_name = 'app/campaign_detail.html'
    context_object_name = 'campaign_detail'
    queryset = models.SaleCampaign.objects.all()

    def get_context_data(self, **kwargs):
        context = {}
        campaign_links = models.SaleLink.objects.filter(campaign=self.object)
        if 'user_public_key' in self.request.GET:
            campaign_links = campaign_links.filter(user_public_key=self.request.GET['user_public_key'])
        context.update({"campaign_links": campaign_links})
        return super().get_context_data(**context)


class CampaignView(generic.FormView):
    template_name = 'app/campaign_submit.html'
    context_object_name = 'campaign_detail'
    queryset = models.SaleCampaign.objects.all()
    success_url = '/view/campaigns'

    def get_form(self, form_class=forms.OnBoardForm):
        return form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.user = self.request.user
        campaign.save()
        return super().form_valid(form)


def sale_link_view(request, url_code):
    link = get_object_or_404(models.SaleLink, url_code=url_code)
    return HttpResponseRedirect(
        redirect_to=f'{link.long_link}'
    )


def click_link_view(request, url_code):
    link = get_object_or_404(models.ClickLink, url_code=url_code)
    transaction = contract_instance.functions.forwardPayPerClickRewards(
        url_code,
        link.campaign.url,
        link.campaign.user_public_key,
        link.user_public_key
    ).buildTransaction({
        'chainId': 3,
        'gas': 320000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': w3.eth.getTransactionCount(settings.ACCOUNT_OWNER_PUBLIC_KEY)}
    )

    txn_signed = w3.eth.account.signTransaction(transaction, private_key=settings.ACCOUNT_OWNER_PRIVATE_KEY)
    w3.eth.sendRawTransaction(txn_signed.rawTransaction)  # thx_hash

    return HttpResponseRedirect(
        redirect_to=f'{link.long_link}'
    )


def link_create_view(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        user_public_key = request.POST['user_public_key']
        campaign = get_object_or_404(models.SaleCampaign, pk=pk)
        if not campaign.links.filter(user_public_key=user_public_key).exists():
            long_link = build_long_link(campaign, request, user_public_key)
            models.SaleLink.objects.create(
                campaign=campaign,
                user_public_key=user_public_key,
                long_link=long_link,
            )
    return HttpResponseRedirect(
        redirect_to=reverse('campaign_detail', args=(pk,))
    )


def build_long_link(campaign, request, user_public_key):
    return f'{campaign.url}?' \
           f'utm_source={request.META["HTTP_HOST"]}{reverse("campaign_detail", args=(campaign.id,))}&' \
           f'utm_medium={user_public_key}&' \
           f'utm_campaign={campaign.name}'


def campaign_create(request):
    # https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}
    context = {}
    if request.user.is_authenticated:
        if hasattr(request.user, 'social_auth') and request.user.social_auth.exists():
            auth_token = request.user.social_auth.last()
            headers = {
                'Authorization': 'Bearer ' + auth_token.access_token
            }
            response = requests.get(
                'https://content.googleapis.com/analytics/v3/management/accounts/~all/webproperties',
                headers=headers
            )
            if response.status_code == 200:
                context.update({"ga_data": response.json()})
    return render(request, 'app/campaign_create.html', context=context)


campaign_submit = CampaignView.as_view()

index = IndexView.as_view()

link_list_view = LinkListView.as_view()
link_detail_view = LinkDetailView.as_view()

campaign_list_view = CampaignListView.as_view()
campaign_detail_view = CampaignDetailView.as_view()
