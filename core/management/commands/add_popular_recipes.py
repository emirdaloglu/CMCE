from django.core.management.base import BaseCommand
from core.models import Recipe, Ingredient

class Command(BaseCommand):
    help = 'Add 4 popular recipes and their ingredients to the database.'

    def handle(self, *args, **options):
        recipes = [
            {
                'name': 'Menemen',
                'image_url': '/static/menemen.jpg',
                'ingredients': [
                    {'name': 'yağ'},
                    {'name': 'soğan'},
                    {'name': 'domates'},
                    {'name': 'tuz'},
                    {'name': 'beyaz peynir'},
                    {'name': 'maydanoz'},
                    {'name': 'yumurta'},
                    {'name': 'kaşar peyniri'},
                ]
            },
            {
                'name': 'Karnıyarık',
                'image_url': '/static/karnıyarık.jpg',
                'ingredients': [
                    {'name': 'patlıcan'},
                    {'name': 'biber'},
                    {'name': 'kıyma'},
                    {'name': 'soğan'},
                    {'name': 'karabiber'},
                    {'name': 'tuz'},
                    {'name': 'domates'},
                    {'name': 'tereyağı'},
                    {'name': 'salça'},
                    {'name': 'yağ'},
                    {'name': 'maydanoz'},
                ]
            },
            {
                'name': 'Mercimek Çorbası',
                'image_url': '/static/mercimek çorbası.jpg',
                'ingredients': [
                    {'name': 'mercimek'},
                    {'name': 'patates'},
                    {'name': 'soğan'},
                    {'name': 'bulyon'},
                    {'name': 'salça'},
                    {'name': 'un'},
                    {'name': 'yağ'},
                ]
            },
            {
                'name': 'Izgara Tavuk',
                'image_url': '/static/ızgara tavuk.jpg',
                'ingredients': [
                    {'name': 'tavuk'},
                    {'name': 'kimyon'},
                    {'name': 'karabiber'},
                    {'name': 'köri'},
                    {'name': 'biber'},
                    {'name': 'yoğurt'},
                    {'name': 'kekik'},
                    {'name': 'yağ'},
                ]
            },
        ]

        # Add new recipes
        recipes += [
            {
                'name': 'Şehriyeli Pirinç Pilavı',
                'image_url': '/static/sehriyeli-pirinc-pilavi.jpg',
                'ingredients': [
                    {'name': 'tereyağı'},
                    {'name': 'sıvı yağ'},
                    {'name': 'pirinç'},
                    {'name': 'arpa şehriye'},
                    {'name': 'sıcak su'},
                    {'name': 'tavuk suyu'},
                    {'name': 'tuz'},
                ]
            },
            {
                'name': 'Brownie Kurabiye',
                'image_url': '/static/brownie-kurabiye-tarifi.jpg',
                'ingredients': [
                    {'name': 'tereyağı'},
                    {'name': 'pudra şekeri'},
                    {'name': 'sıvı yağ'},
                    {'name': 'vanilya'},
                    {'name': 'kabartma tozu'},
                    {'name': 'kakao'},
                    {'name': 'un'},
                    {'name': 'yumurta'},
                    {'name': 'su'},
                    {'name': 'toz şeker'},
                ]
            },
            {
                'name': 'Patatesli Çıtır Börek',
                'image_url': '/static/patatesli-citir-borek-tarifi.jpg',
                'ingredients': [
                    {'name': 'yufka'},
                    {'name': 'sıvı yağ'},
                    {'name': 'sirke'},
                    {'name': 'un'},
                    {'name': 'patates'},
                    {'name': 'soğan'},
                    {'name': 'nane'},
                    {'name': 'kırmızı toz biber'},
                    {'name': 'pul biber'},
                    {'name': 'karabiber'},
                    {'name': 'tuz'},
                    {'name': 'yumurta'},
                ]
            },
            {
                'name': 'Acıbadem Kurabiye',
                'image_url': '/static/acibadem-kurabiye.jpg',
                'ingredients': [
                    {'name': 'çiğ badem'},
                    {'name': 'toz şeker'},
                    {'name': 'yumurta beyazı'},
                    {'name': 'nişasta'},
                    {'name': 'limon suyu'},
                ]
            },
            {
                'name': 'Un Kurabiyesi',
                'image_url': '/static/un-kurabiyesi.jpg',
                'ingredients': [
                    {'name': 'tereyağı'},
                    {'name': 'margarin'},
                    {'name': 'sıvı yağ'},
                    {'name': 'buğday nişastası'},
                    {'name': 'pudra şekeri'},
                    {'name': 'un'},
                ]
            },
            {
                'name': 'Yalancı Boyoz',
                'image_url': '/static/yalanci-boyoz.jpg',
                'ingredients': [
                    {'name': 'yufka'},
                    {'name': 'sıvı yağ'},
                    {'name': 'su'},
                    {'name': 'beyaz peynir'},
                    {'name': 'soda'},
                    {'name': 'tuz'},
                    {'name': 'yumurta sarısı'},
                ]
            },
            {
                'name': 'Havuçlu Cevizli Tarçınlı Kek',
                'image_url': '/static/havuclu-cevizli-tarcinli-kek.jpg',
                'ingredients': [
                    {'name': 'yumurta'},
                    {'name': 'şeker'},
                    {'name': 'sıvı yağ'},
                    {'name': 'süt'},
                    {'name': 'un'},
                    {'name': 'vanilya'},
                    {'name': 'kabartma tozu'},
                    {'name': 'havuç'},
                    {'name': 'ceviz'},
                    {'name': 'tarçın'},
                ]
            },
            {
                'name': 'Pastane Poğaçası',
                'image_url': '/static/pastane-pogacasi.jpg',
                'ingredients': [
                    {'name': 'margarin'},
                    {'name': 'tereyağı'},
                    {'name': 'instant maya'},
                    {'name': 'süt'},
                    {'name': 'tuz'},
                    {'name': 'sıvı yağ'},
                    {'name': 'yumurta'},
                    {'name': 'şeker'},
                    {'name': 'un'},
                    {'name': 'peynir'},
                ]
            },
            {
                'name': 'Dereotlu Poğaça',
                'image_url': '/static/dereotlu-pogaca.jpg',
                'ingredients': [
                    {'name': 'sıvı yağ'},
                    {'name': 'yoğurt'},
                    {'name': 'kabartma tozu'},
                    {'name': 'tuz'},
                    {'name': 'dereotu'},
                    {'name': 'yumurta'},
                    {'name': 'un'},
                ]
            },
            {
                'name': 'Pankek',
                'image_url': '/static/pankek.jpg',
                'ingredients': [
                    {'name': 'yumurta'},
                    {'name': 'şeker'},
                    {'name': 'süt'},
                    {'name': 'un'},
                    {'name': 'kabartma tozu'},
                    {'name': 'vanilya'},
                    {'name': 'sıvı yağ'},
                ]
            },
            {
                'name': 'Sütlü Domates Çorbası',
                'image_url': '/static/sutlu-domates-corbasi.jpg',
                'ingredients': [
                    {'name': 'sıvı yağ'},
                    {'name': 'tereyağı'},
                    {'name': 'un'},
                    {'name': 'domates salçası'},
                    {'name': 'domates'},
                    {'name': 'su'},
                    {'name': 'süt'},
                    {'name': 'tuz'},
                ]
            },
            {
                'name': 'Havuç Tarator',
                'image_url': '/static/havuc-tarator.jpg',
                'ingredients': [
                    {'name': 'havuç'},
                    {'name': 'sıvı yağ'},
                    {'name': 'sarımsak'},
                    {'name': 'yoğurt'},
                    {'name': 'tuz'},
                ]
            },
        ]

        for rec in recipes:
            recipe, created = Recipe.objects.get_or_create(
                name=rec['name'],
                defaults={'image_url': rec['image_url']}
            )
            if not created:
                recipe.image_url = rec['image_url']
                recipe.save()
            for ing in rec['ingredients']:
                Ingredient.objects.get_or_create(recipe=recipe, name=ing['name'])
        self.stdout.write(self.style.SUCCESS('Popular recipes and ingredients added.')) 