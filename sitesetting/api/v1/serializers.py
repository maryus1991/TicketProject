from sitesetting.models import Contact, Team , Site
from rest_framework.serializers import ModelSerializer



class SiteSettingsSerializers(ModelSerializer):
    """
    serializers for site settings
    """

    class Meta:
        model = Site
        fields = '__all__'


        
class ContactSerializers(ModelSerializer):
    """
    serializers for contact
    """

    class Meta:
        model = Contact
        fields = '__all__'


class TeamSerializers(ModelSerializer):
    """
    serializers for team
    """

    class Meta:
        model = Team
        fields = '__all__'
 

