from django.db import models
from django.contrib.auth.models import User
from local.models import Mesa
from local.models import Cliente
from carta.models import Plato

class Comanda(models.Model):
	mesa      = models.ForeignKey(Mesa)
	cliente   = models.ForeignKey(Cliente)
	encargado = models.ForeignKey(User)
	personas  = models.IntegerField()
	activa    = models.BooleanField(default=True)
	fecha     = models.DateTimeField(auto_now=True,auto_now_add=True)

	def __unicode__(self):
		return ('%s con %d personas') % (self.mesa, self.personas)

class Pedido(models.Model):
	plato    = models.ForeignKey(Plato)
	cantidad = models.IntegerField(default=1)
	comanda  = models.ForeignKey(Comanda)

	def __unicode__(self):
		return ('%d platos de %s') % (self.cantidad, self.plato)

class Comprobante(models.Model):
	TIPO_OPCIONES = (
		('BOL', 'Boleta'),
		('FAC', 'Factura')
	)
	tipo      = models.CharField(max_length=3,choices=TIPO_OPCIONES,default='BOL')
	descuento = models.DecimalField(max_digits=5,decimal_places=2,default=0,blank=True,null=True)
	propina   = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	igv       = models.DecimalField(max_digits=5,decimal_places=2,default=0)
	subtotal  = models.DecimalField(max_digits=5,decimal_places=2,default=0)
	total     = models.DecimalField(max_digits=5,decimal_places=2,default=0)
	comanda   = models.ForeignKey(Comanda)

	def save(self,*args,**kwargs):
		total = 0
		Pedidos = Pedido.objects.filter(comanda=self.comanda)
		for item in Pedidos:
			total = total + (item.plato.precio*item.cantidad)

		self.total    = float(total)
		self.subtotal = float(total) / 1.18
		self.igv      = float(total) - (float(total) / 1.18)
		super(Comprobante, self).save(*args, **kwargs)