from django.db import models

class Scrape(models.Model):
    date = models.DateField(auto_now_add=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)
    is_finished = models.BooleanField(null=True)
    STATUS_CHOICES = (
        (0, 'Unknown'),
        (1, 'Success'),
        (2, 'HTTPError'),
        (3, 'URLError'),
        (4, 'Others'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    status_info = models.TextField(null=True)
    class Meta:
        db_table = 'scrapes'
    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

class Item(models.Model):
    product_id = models.IntegerField(db_index=True, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False)
    current_price = models.IntegerField(null=True)
    diff_price_prev = models.IntegerField(null=True)
    scrape_0 = models.ForeignKey(Scrape, related_name='scrape_0', on_delete=models.CASCADE, null=True)
    price_0 = models.IntegerField(null=True)
    scrape_1 = models.ForeignKey(Scrape, related_name='scrape_1', on_delete=models.CASCADE, null=True)
    price_1 = models.IntegerField(null=True)
    scrape_2 = models.ForeignKey(Scrape, related_name='scrape_2', on_delete=models.CASCADE, null=True)
    price_2 = models.IntegerField(null=True)
    scrape_3 = models.ForeignKey(Scrape, related_name='scrape_3', on_delete=models.CASCADE, null=True)
    price_3 = models.IntegerField(null=True)
    class Meta:
        db_table = 'items'
    def __str__(self):
        return self.name
    def get_trends(self):
        trends = {}
        if self.scrape_0:
            trends[str(self.scrape_0.date)] = self.price_0
        if self.scrape_1:
            trends[str(self.scrape_1.date)] = self.price_1
        if self.scrape_2:
            trends[str(self.scrape_2.date)] = self.price_2
        if self.scrape_3:
            trends[str(self.scrape_3.date)] = self.price_3
        trends = sorted(trends.items())
        return trends