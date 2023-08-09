from django.contrib import admin
from django.contrib.admin.options import ModelAdmin   #(model admini inherti edecegiz)
from .models import *

#-----------------------------
# Category
#-----------------------------
admin.site.register(Category)


#-----------------------------
# Product
#-----------------------------
class ReviewInline(admin.TabularInline):
    model = Review #ForeignKey modelName
    extra = 1 #yeni yorum ekleme alani 1 tane
    classes=["collapse"]




class ProductAdmin(ModelAdmin):
    #Tablo stunlari
    list_display=["id","name", "description", "is_in_stock", "create_date", "update_date"]
    #Tablo üzerinde güncelleyebilme
    list_editable=["is_in_stock"]
    #Kayda gitmek icin linkleme
    list_display_links=["id", "name"]
    #Filtreleme (arama degil)
    list_filter=["is_in_stock", "create_date", "update_date"]
    #Arama
    search_fields=["id", "name"]
    #Armaa bilgilendirme yazisi
    search_help_text="Arama yapmak icin burayi kullanin"
    #Default siralama
    ordering=["-id"]  #"id" ASC -> "" "-id" DESC  (ters siralama yaptik)
    #Sayfa basina kayit sayisi 
    list_per_page= 20
    #tümünü göster yaparken max sayisi
    list_max_show_all=200
    #Tarihe göre filtreleme basligi 
    date_hierarchy="create_date"  #Tarih field olmak zorunda list icine alinmaz tek bir durum yazilir. 
    #Otomatik kayiz olustur
    prepopulated_fields = {"slug": ["name", "is_in_stock"]}
    #form liste görüntüleme
    fields=(
        ("name", "is_in_stock"),
        ("slug"),
        ("categories"),
        ("description"),
    ) 
    # filter_vertical =["categories"]
    filter_horizontal =["categories"]
    #detayli form liste görüntüleme
    '''fieldsets=(
        ("General Settings", {
            "fields":(
                ("name", "is_in_stock"),
                ("slug"),
            )
       }),
        ("Optional Settings", {
            "classes":["collapse"], #description bununla gizleniyor show hide yapiyoruz kutu acip kapaniyor
            
            "fields":(
                ("description"),
            ),
            "description":"description yazarak fieldsets kullanarak aciklama ekledik"
       }),
    )'''
   #iceriye bir veri aktaracagim o veriyi reviewinline icine al:
    inlines = [ReviewInline]

#iki metod yazdik bu metotlarda birinde isaretli olanlar stokta var yapsin dedik digerini de tam tesini yaptik
    def set_stock_in(self, request, queryset):
       count = queryset.update(is_in_stock=True)
       self.message_user(request, f'{count} adet "Stokta var" olarak isaretlendi' )


    def set_stock_out(self, request, queryset):
       count = queryset.update(is_in_stock=False)
       self.message_user(request, f'{count} adet "Stokta yok" olarak isaretlendi' )

# bu mettolari admin panalede göstermek icin action() menüsünü kulllanacagiz 
    actions=("set_stock_in", "set_stock_out")
    #kutunun icindeki isimleri degisebiliriz.
    set_stock_in.short_description ="isaretli ürünleri stoga ekle"
    set_stock_out.short_description ="isaretli ürünleri stoktan cikar"


#ürün kac gün önce eklendi metodu
    def added_days_ago(self, object):
        from django.utils import timezone
        different = timezone.now() - object.create_date
        return different.days
    
    # list_display=["id","name", "description", "is_in_stock", "create_date", "update_date", "added_days_ago"]
    list_display += ["added_days_ago"]
admin.site.register(Product, ProductAdmin)



#----------------------------
# Review
#----------------------------

class ReviewAdmin(ModelAdmin):
    list_display = ["__str__", "created_date"]
    raw_id_fields=["product"]

admin.site.register(Review, ReviewAdmin)