import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from . import models, forms


class IndexView(generic.TemplateView):
    template_name = 'app/index.html'


class LinkListView(generic.ListView):
    template_name = 'app/link_list.html'
    context_object_name = 'link_list'
    queryset = models.Link.objects.all()


class LinkDetailView(generic.DetailView):
    template_name = 'app/link_detail.html'
    context_object_name = 'link_detail'
    queryset = models.Link.objects.all()


class CampaignListView(generic.ListView):
    template_name = 'app/campaign_list.html'
    context_object_name = 'campaign_list'
    queryset = models.Campaign.objects.all()


class CampaignDetailView(generic.DetailView):
    template_name = 'app/campaign_detail.html'
    context_object_name = 'campaign_detail'
    queryset = models.Campaign.objects.all()

    def get_context_data(self, **kwargs):
        context = {}
        if self.request.user.is_authenticated:
            campaign_links = models.Link.objects.filter(
                user=self.request.user,
                campaign=self.object
            )
            context.update({"campaign_links": campaign_links})
        return super().get_context_data(**context)


class CampaignView(generic.FormView):
    template_name = 'app/campaign_submit.html'
    context_object_name = 'campaign_detail'
    queryset = models.Campaign.objects.all()
    success_url = '/campaigns'

    def get_form(self, form_class=forms.OnBoardForm):
        return form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.user = self.request.user
        campaign.save()
        return super().form_valid(form)


def link_view(request, url_code):
    link = get_object_or_404(models.Link, url_code=url_code)
    return HttpResponseRedirect(
        redirect_to=f'{link.long_link}'
    )


def link_create_view(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        user_public_key = request.POST['user_public_key']
        campaign = get_object_or_404(models.Campaign, pk=pk)
        if not campaign.links.filter(user=request.user).exists():
            long_link = build_long_link(campaign, request, user_public_key)
            models.Link.objects.create(
                campaign=campaign,
                user=request.user,
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
