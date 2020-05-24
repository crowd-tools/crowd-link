from django import forms

from app import models


class OnBoardForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'crowdlink-my-project'}))
    url = forms.URLField(label='URL for campaign')
    reward = forms.DecimalField(label='Reward', decimal_places=10, max_digits=18, initial=1)

    class Meta:
        model = models.SaleCampaign
        fields = ('name', 'url', 'reward', 'google_view_id')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if user.is_authenticated and user.social_auth.exists():
        #     auth_token = user.social_auth.last()
        #     headers = {
        #         'Authorization': 'Bearer ' + auth_token.access_token
        #     }
        #     response = requests.get(
        #         'https://content.googleapis.com/analytics/v3/management/accounts/~all/webproperties',
        #         headers=headers
        #     )
        #     if response.status_code == 200:
        #         google_property_choices = []
        #         response_json = response.json()
        #         for item in response_json.get("items", []):
        #             google_property_choices.append((item['id'], item['websiteUrl']))
        #
        #         self.fields['google_property'].choices = google_property_choices
