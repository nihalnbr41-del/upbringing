

from django.core.management.base import BaseCommand


from core.models import Product


class Command(BaseCommand):
    
    help = "Add sample maternity and newborn products."

    def handle(self, *args, **options):

        
        items = [
            (
                "Maternity Support Pillow",
                "Maternity",
                "Comfortable support for rest and side sleeping.",
                "1299.00",
                "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=900",
            ),
            (
                "Reusable Nursing Pads",
                "Maternity",
                "Soft reusable pads for everyday comfort.",
                "399.00",
                "https://images.unsplash.com/photo-1604881988758-f76ad2f7aac1?w=900",
            ),
            (
                "Newborn Cotton Wrap",
                "Newborn",
                "Gentle cotton wrap for supervised swaddling.",
                "549.00",
                "https://images.unsplash.com/photo-1519689680058-324335c77eba?w=900",
            ),
            (
                "Baby Care Starter Kit",
                "Newborn",
                "A simple starter kit for everyday baby care.",
                "799.00",
                "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=900",
            ),
            (
                "Pregnancy Journal",
                "Wellbeing",
                "A place to record milestones and reflections.",
                "299.00",
                "https://i.pinimg.com/736x/5e/33/f6/5e33f6984d9a9706f3db951a2703f359.jpg",
            ),
            (
                "Soft Baby Blanket",
                "Newborn",
                "A soft blanket; follow safe-sleep guidance and keep loose bedding out of an infant sleep space.",
                "699.00",
                "https://images.unsplash.com/photo-1519689680058-324335c77eba?w=900",
            ),
        ]


        for name, category, description, price, image_url in items:
            Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "description": description,
                    "price": price,
                    "image_url": image_url,
                },
            )

       
        self.stdout.write(
            self.style.SUCCESS("Sample products added.")
        )
