from django import forms
from ibroker.models import Stock,Quote
class UploadQuotesFile(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()







#Todo melhorar e colocar um jeito de o usuário ver o custo total da operação
#Acredito que deva ser feito no html, da pra fazer sem ajax se carregar todos os preços com uma lista ou algo assim
class OrderForm(forms.Form):
    stocks = Stock.objects.all()
    choices = [(stock.id,stock.stock_code) for stock in stocks]
    stock = forms.ChoiceField(label='Stock: ',choices=choices)
    #price = forms.DecimalField(label='Price: ')
    qtd = forms.IntegerField(label='Quantidade',min_value=1)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()

        qtd = cleaned_data["qtd"]
        stockId = cleaned_data["stock"]

        stock = Stock.objects.get(pk=stockId)
        quote = Quote.objects.filter(stock=stock.id).order_by('-quote_datetime')[0]
        if not quote:
            raise forms.ValidationError(
                "There isn't a quote for {0}.".format(stock.stock_code)
            )

        if quote:
            # if quote.price*qtd>self.user.get_amount_cash:
            if quote.price*qtd>self.user.get_amount_cash():
                raise forms.ValidationError(
                        "You don't have enough money to buy {0} of {1}.".format(qtd,stock.stock_code)
                    )

        return cleaned_data


