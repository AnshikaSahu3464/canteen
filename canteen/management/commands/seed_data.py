from django.core.management.base import BaseCommand
from canteen.models import Category, MenuItem, Ingredient


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding canteen data...')

        categories = [
            {'name': 'Breakfast',   'icon': '🌅', 'slug': 'breakfast',   'order': 1},
            {'name': 'Lunch',       'icon': '🍱', 'slug': 'lunch',       'order': 2},
            {'name': 'Snacks',      'icon': '🍿', 'slug': 'snacks',      'order': 3},
            {'name': 'Drinks',      'icon': '🥤', 'slug': 'drinks',      'order': 4},
            {'name': 'Desserts',    'icon': '🍰', 'slug': 'desserts',    'order': 5},
            {'name': 'Packed Food', 'icon': '📦', 'slug': 'packed-food', 'order': 6},
        ]

        for cat_data in categories:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'  Created category: {cat.name}')
            else:
                self.stdout.write(f'  Already exists: {cat.name}')

        items = [
            {'category': 'breakfast', 'name': 'Poha',
             'price': 30, 'is_veg': True, 'stock': 50,
             'desc': 'Flattened rice with spices and peanuts'},
            {'category': 'breakfast', 'name': 'Idli Sambar',
             'price': 40, 'is_veg': True, 'stock': 40,
             'desc': '2 soft idlis with sambar and chutney'},
            {'category': 'breakfast', 'name': 'Paratha',
             'price': 50, 'is_veg': True, 'stock': 30,
             'desc': 'Stuffed wheat flatbread with curd'},
            {'category': 'breakfast', 'name': 'Bread Toast',
             'price': 25, 'is_veg': True, 'stock': 60,
             'desc': 'Buttered toast with jam'},
            {'category': 'lunch', 'name': 'Dal Rice',
             'price': 60, 'is_veg': True, 'stock': 50,
             'desc': 'Dal tadka with steamed rice'},
            {'category': 'lunch', 'name': 'Rajma Chawal',
             'price': 70, 'is_veg': True, 'stock': 40,
             'desc': 'Kidney beans curry with rice'},
            {'category': 'lunch', 'name': 'Veg Thali',
             'price': 90, 'is_veg': True, 'stock': 30,
             'desc': 'Rice dal sabzi roti and salad'},
            {'category': 'lunch', 'name': 'Chicken Curry',
             'price': 100, 'is_veg': False, 'stock': 25,
             'desc': 'Spicy chicken curry with roti'},
            {'category': 'lunch', 'name': 'Egg Fried Rice',
             'price': 80, 'is_veg': False, 'stock': 35,
             'desc': 'Wok tossed egg fried rice'},
            {'category': 'snacks', 'name': 'Samosa',
             'price': 15, 'is_veg': True, 'stock': 80,
             'desc': 'Crispy fried pastry with potato'},
            {'category': 'snacks', 'name': 'Vada Pav',
             'price': 20, 'is_veg': True, 'stock': 60,
             'desc': 'Mumbai style potato burger'},
            {'category': 'snacks', 'name': 'Bread Pakoda',
             'price': 20, 'is_veg': True, 'stock': 50,
             'desc': 'Stuffed bread deep fried in batter'},
            {'category': 'snacks', 'name': 'French Fries',
             'price': 50, 'is_veg': True, 'stock': 40,
             'desc': 'Crispy golden fries with ketchup'},
            {'category': 'snacks', 'name': 'Pav Bhaji',
             'price': 60, 'is_veg': True, 'stock': 30,
             'desc': 'Spiced vegetable mash with butter pav'},
            {'category': 'drinks', 'name': 'Chai',
             'price': 10, 'is_veg': True, 'stock': 100,
             'desc': 'Hot masala tea'},
            {'category': 'drinks', 'name': 'Coffee',
             'price': 20, 'is_veg': True, 'stock': 80,
             'desc': 'Hot filter coffee'},
            {'category': 'drinks', 'name': 'Lassi',
             'price': 30, 'is_veg': True, 'stock': 50,
             'desc': 'Sweet chilled yogurt drink'},
            {'category': 'drinks', 'name': 'Lemonade',
             'price': 25, 'is_veg': True, 'stock': 60,
             'desc': 'Fresh lime soda'},
            {'category': 'drinks', 'name': 'Mango Shake',
             'price': 50, 'is_veg': True, 'stock': 30,
             'desc': 'Thick mango milkshake'},
            {'category': 'desserts', 'name': 'Gulab Jamun',
             'price': 30, 'is_veg': True, 'stock': 40,
             'desc': '2 pieces soft gulab jamun'},
            {'category': 'desserts', 'name': 'Halwa',
             'price': 25, 'is_veg': True, 'stock': 30,
             'desc': 'Semolina dessert with dry fruits'},
            {'category': 'desserts', 'name': 'Ice Cream',
             'price': 40, 'is_veg': True, 'stock': 50,
             'desc': '2 scoops of vanilla ice cream'},
            {'category': 'packed-food', 'name': 'Biscuit Pack',
             'price': 20, 'is_veg': True, 'stock': 4,
             'is_packed': True, 'desc': 'Assorted biscuits pack'},
            {'category': 'packed-food', 'name': 'Chips Packet',
             'price': 20, 'is_veg': True, 'stock': 3,
             'is_packed': True, 'desc': '30g salted chips'},
            {'category': 'packed-food', 'name': 'Juice Box',
             'price': 30, 'is_veg': True, 'stock': 15,
             'is_packed': True, 'desc': '200ml fruit juice pack'},
            {'category': 'packed-food', 'name': 'Noodles Cup',
             'price': 35, 'is_veg': True, 'stock': 20,
             'is_packed': True, 'desc': 'Instant cup noodles'},
        ]

        for item_data in items:
            cat_slug  = item_data.pop('category')
            stock     = item_data.pop('stock')
            desc      = item_data.pop('desc', '')
            is_packed = item_data.pop('is_packed', False)
            try:
                cat = Category.objects.get(slug=cat_slug)
                item, created = MenuItem.objects.get_or_create(
                    name=item_data['name'],
                    category=cat,
                    defaults={
                        'price':          item_data['price'],
                        'is_veg':         item_data['is_veg'],
                        'stock_quantity': stock,
                        'description':    desc,
                        'is_packed':      is_packed,
                        'is_available':   True,
                    }
                )
                if created:
                    self.stdout.write(f'  Created: {item.name}')
                else:
                    self.stdout.write(f'  Already exists: {item.name}')
            except Category.DoesNotExist:
                self.stdout.write(f'  Category not found: {cat_slug}')

        ingredients = [
            {'name': 'Rice',        'unit': 'kg',     'current': 20,  'min': 5},
            {'name': 'Wheat Flour', 'unit': 'kg',     'current': 15,  'min': 5},
            {'name': 'Dal',         'unit': 'kg',     'current': 3,   'min': 4},
            {'name': 'Milk',        'unit': 'liters', 'current': 10,  'min': 5},
            {'name': 'Cooking Oil', 'unit': 'liters', 'current': 2,   'min': 3},
            {'name': 'Sugar',       'unit': 'kg',     'current': 8,   'min': 2},
            {'name': 'Tea Leaves',  'unit': 'grams',  'current': 500, 'min': 200},
            {'name': 'Potatoes',    'unit': 'kg',     'current': 10,  'min': 3},
        ]

        for ing_data in ingredients:
            ing, created = Ingredient.objects.get_or_create(
                name=ing_data['name'],
                defaults={
                    'unit':             ing_data['unit'],
                    'current_stock':    ing_data['current'],
                    'minimum_required': ing_data['min'],
                }
            )
            if created:
                self.stdout.write(f'  Ingredient: {ing.name}')

        self.stdout.write(self.style.SUCCESS('\nSeeding complete!'))