from django.core.management.base import BaseCommand
from core.models import Recipe, Ingredient

class Command(BaseCommand):
    help = 'Add 4 popular recipes and their ingredients to the database.'

    def handle(self, *args, **options):
        recipes = [
            {
                'name': 'Menemen',
                'image_url': '/static/menemen.jpg',
                'url': 'https://www.nefisyemektarifleri.com/video/menemen-nasil-yapilir/',
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
                'url': 'https://www.nefisyemektarifleri.com/video/bostan-patlicanindan-firinda-karniyarik/',
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
                'url': 'https://www.nefisyemektarifleri.com/mercimek-corbasi-tarifi/',
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
                'url': 'https://www.nefisyemektarifleri.com/izgara-lezzetinde-tavada-tavuk-but/',
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
            {
                'name': 'Şehriyeli Pirinç Pilavı',
                'image_url': '/static/sehriyeli-pirinc-pilavi.jpg',
                'url': 'https://www.nefisyemektarifleri.com/video/sehriyeli-pirinc-pilavi-nasil-yapilir/',
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
                'url': 'https://www.nefisyemektarifleri.com/video/brownie-kurabiye-tarifi/',
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
                'url': 'https://www.nefisyemektarifleri.com/patatesli-citir-borek-tarifi/',
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
                'url': 'https://www.nefisyemektarifleri.com/acibadem-kurabiye/',
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
                'url': 'https://www.nefisyemektarifleri.com/agizda-dagilan-pastane-un-kurabiyesi/',
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
                'url': 'https://www.nefisyemektarifleri.com/video/yalanci-boyoz-tarifi/',
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
                'url': 'https://www.nefisyemektarifleri.com/video/havuclu-cevizli-tarcinli-kek-yapimi/',
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
                'url': 'https://www.nefisyemektarifleri.com/video/pastane-pogacasi-tarifi/',
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
                'url': 'https://www.nefisyemektarifleri.com/dereotlu-pogaca/',
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
                'url': 'https://www.nefisyemektarifleri.com/video/pankek-tarifi-videosu/',
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
                'url': 'https://www.nefisyemektarifleri.com/video/sutlu-domates-corbasi-tarifi/',
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
                'url': 'https://www.nefisyemektarifleri.com/havuc-tarator-tarifi-3/',
                'ingredients': [
                    {'name': 'havuç'},
                    {'name': 'sıvı yağ'},
                    {'name': 'sarımsak'},
                    {'name': 'yoğurt'},
                    {'name': 'tuz'},
                ]
            },
            {
                'name': 'Yoğurt Çorbası',
                'image_url': '/static/yogurt-corbasi.jpg',
                'url': 'https://www.nefisyemektarifleri.com/video/yogurt-corbasi-kesinlikle-deneyin-mukemmel-oluyor-videolu/',
                'ingredients': [
                    {'name': 'yoğurt'},
                    {'name': 'un'},
                    {'name': 'su'},
                    {'name': 'erişte'},
                    {'name': 'tuz'},
                    {'name': 'tereyağı'},
                    {'name': 'kırmızı toz biber'},
                    {'name': 'nane'},
                ]
            },
            {
                'name': 'Patatesli Sulu Köfte',
                'image_url': '/static/patatesli-sulu-kofte.jpg',
                'url': 'https://www.nefisyemektarifleri.com/video/patatesli-sulu-kofte-yemegi-videosu/',
                'ingredients': [
                    {'name': 'kıyma'},
                    {'name': 'patates'},
                    {'name': 'soğan'},
                    {'name': 'pilavlık bulgur'},
                    {'name': 'domates salçası'},
                    {'name': 'sıvı yağ'},
                    {'name': 'un'},
                    {'name': 'sarımsak'},
                    {'name': 'tuz'},
                    {'name': 'karabiber'},
                    {'name': 'pul biber'},
                    {'name': 'kırmızı biber'},
                ]
            },
            {
                'name': 'Mor Lahana Mezesi',
                'image_url': '/static/mor-lahana-mezesi.jpg',
                'url': 'https://www.nefisyemektarifleri.com/video/mor-lahana-mezesi-videolu-anlatimi/',
                'ingredients': [
                    {'name': 'kırmızı lahana'},
                    {'name': 'sıvı yağ'},
                    {'name': 'yoğurt'},
                    {'name': 'mayonez'},
                    {'name': 'tuz'},
                    {'name': 'sarımsak'},
                ]
            },
            {
                'name': 'Mantı',
                'image_url': '/static/manti.jpg',
                'url': 'https://www.nefisyemektarifleri.com/video/manti-tarifi-videosu/',
                'ingredients': [
                    {'name': 'un'},
                    {'name': 'su'},
                    {'name': 'yumurta'},
                    {'name': 'kıyma'},
                    {'name': 'soğan'},
                    {'name': 'karabiber'},
                    {'name': 'pul biber'},
                    {'name': 'tuz'},
                    {'name': 'tereyağı'},
                    {'name': 'salça'},
                    {'name': 'yoğurt'},
                    {'name': 'sarımsak'},
                    {'name': 'nane'},
                    {'name': 'sumak'},
                ]
            },
        ]

        for rec in recipes:
            recipe, created = Recipe.objects.get_or_create(
                name=rec['name'],
                defaults={'image_url': rec['image_url'], 'url': rec.get('url', '')}
            )
            if not created:
                recipe.image_url = rec['image_url']
                recipe.url = rec.get('url', '')
                recipe.save()
            for ing in rec['ingredients']:
                Ingredient.objects.get_or_create(recipe=recipe, name=ing['name'])
        self.stdout.write(self.style.SUCCESS('Popular recipes and ingredients added.')) 