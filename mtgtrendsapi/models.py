from django.db import models

class Scrapes(models.Model):
    date = models.DateField(auto_now_add=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)
    is_finished = models.BooleanField(null=True)

class Items(models.Model):
    product_id = models.IntegerField(db_index=True, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False)
    diff_price_prev = models.IntegerField(null=True)
    scrape_0 = models.ForeignKey(Scrapes, related_name='scrape_0', on_delete=models.CASCADE, null=True)
    price_0 = models.IntegerField(null=True)
    scrape_1 = models.ForeignKey(Scrapes, related_name='scrape_1', on_delete=models.CASCADE, null=True)
    price_1 = models.IntegerField(null=True)
    scrape_2 = models.ForeignKey(Scrapes, related_name='scrape_2', on_delete=models.CASCADE, null=True)
    price_2 = models.IntegerField(null=True)
    scrape_3 = models.ForeignKey(Scrapes, related_name='scrape_3', on_delete=models.CASCADE, null=True)
    price_3 = models.IntegerField(null=True)
    def __str__(self):
        return self.name