from django.shortcuts import render
from django.http import HttpResponse

from AppCovid.models import Guantes, Oximetros, Barbijos
from AppCovid.forms import BarbijosFormulario, GuantesFormulario, UserRegisterForm

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.decorators import login_required

# Create your views here.

def inicio(request):

    return render(request, "AppCovid/inicio.html")

def guantes(request):

    return render(request, "AppCovid/guantes.html")

def barbijos(request):
    
    return render(request, "AppCovid/barbijos.html")

def oximetros(request):
    
    return render(request, "AppCovid/oximetros.html")

def barbijosFormulario(request):
    if request.method == "POST":

        miFormulario = BarbijosFormulario(request.POST)
        
        if miFormulario.is_valid():

            informacion= miFormulario.cleaned_data

            barbijoInst= Barbijos(marca= informacion["marca"], tamanio= informacion["tamanio"], precio= request.POST ["precio"])

            barbijoInst.save()  

            return render(request,"AppCovid/inicio.html")

    else:

        miFormulario = BarbijosFormulario()

    return render(request, "AppCovid/barbijosFormulario.html", {"miFormulario": miFormulario})

def busquedaDeBarbijos(request):

    return render(request, "AppCovid/busquedaDeBarbijos.html")


def buscar(request):

    if request.GET["marca"]:
        
        marca= request.GET["marca"]

        barbijo= Barbijos.objects.filter(marca__icontains= marca)

    #respuesta= f"Estoy buscando a: {request.GET['marca']}"
        return render(request, "AppCovid/resultadoBusqueda.html", {"barbijo": barbijo, "marca":marca})
    else: 
        respuesta= "Por favor mandame mas informacion, sino no puedo ayudarte"
    return HttpResponse(respuesta)


@login_required
def leerGuantes(request):

    guante= Guantes.objects.all()

    diccionario1= {"guante": guante}
    
    return render(request, "AppCovid/leerGuantes.html",diccionario1)


def guantesFormulario(request):
    if request.method == "POST":

        miFormulario = GuantesFormulario(request.POST)
        
        if miFormulario.is_valid():

            informacion= miFormulario1.cleaned_data

            guanteInst= Guantes(marca= informacion["marca"], tamanio= informacion["tamanio"], precio= request.POST ["precio"], esPremium= request.POST["esPremium"])

            guanteInst.save()  

            return render(request,"AppCovid/inicio.html")

    else:

        miFormulario = GuantesFormulario()

    return render(request, "AppCovid/guantesFormulario.html", {"miFormulario": miFormulario})

def eliminarGuante(request, marca_para_borrar ):

    guanteQueQuieroBorrar= Guantes.objects.get(marca= marca_para_borrar)

    guanteQueQuieroBorrar.delete()

    guante =Guantes.objects.all()

    return render(request, "AppCovid/leerGuantes.html", {"guante": guante})

def editarGuante(request, marca_para_editar):

    guanteAEditar= Guantes.objects.get(marca=marca_para_editar)

    if request.method == "POST":

            miFormulario = GuantesFormulario(request.POST)
            
            if miFormulario.is_valid():

                informacion3= miFormulario.cleaned_data

            
                guanteAEditar.marca= informacion3["marca"]
                guanteAEditar.tamanio= informacion3["tamanio"]
                guanteAEditar.precio= informacion3["precio"]
                guanteAEditar.esPremium= informacion3["esPremium"]
                

                guanteAEditar.save()

                return render(request,"AppCovid/inicio.html")

    else:

        miFormulario = GuantesFormulario(initial={"marca": guanteAEditar.marca, "tamanio": guanteAEditar.tamanio, "precio": guanteAEditar.precio, "esPremium": guanteAEditar.esPremium})

    return render(request, "AppCovid/editarGuante.html", {"miFormulario": miFormulario, "marca_para_editar": marca_para_editar})

#class GuantesList(ListView):
    #model= Guantes
    #template_name= "AppCovid/guantes_list.html"

#class GuantesDetalle(DetailView):
    #model= Guantes
    #template_name= "AppCovid/guantes_detalle.html"
class OximetrosList(ListView):
    
    model = Oximetros
    template_name = "AppCoder/oximetros_list.html"
    
#Detalle - SUPER Leer - Buscar!!!!!
class OximetrosDetalle(DetailView):
    
    model = Oximetros
    template_name = "AppCoder/oximetros_detalle.html"
    
#Crear elementos
class OximetrosCreacion(CreateView):
    
    model = Oximetros
    success_url = "../oximetros/list"  #AppCoder/template/AppCoder/editar
    fields = ["marca", "origen", "precio", "esImportado"]
    
#modificar!!!!!!!!!!!  
class OximetrosUpdate(UpdateView):
    
    model = Oximetros
    success_url = "../oximetros/list"
    fields = ["marca", "origen", "precio", "esImportado"]
  
#Borrar   
class OximetrosDelete(DeleteView):
    
    model = Oximetros
    success_url = "../oximetros/list"

def login_request(request):
    
    if request.method =="POST":
        
        form = AuthenticationForm(request, data = request.POST)
        
        if form.is_valid():
            
            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            
            user = authenticate(username=usuario, password = contra)
            
            if user is not None:
                
                login(request, user)
                
                return render(request, "AppCovid/inicio.html", {"mensaje":f"BIENVENIDO AL PORTAL, {usuario}!!!!"})
                
            else:
                
                return render(request, "AppCovid/inicio.html", {"mensaje":f"DATOS INCORRECTOS"})
                
            
        else:
            
            return render(request, "AppCovid/inicio.html", {"mensaje":f"Formulario Erroneo"})
            
            
    
    
    form = AuthenticationForm()  #Formulario sin nada para hacer el login
    
    return render(request, "AppCovid/login.html", {"form":form} )


def register(request):

    if request.method == "POST":
        #form= UserCreationForm(request.POST)
        form= UserRegisterForm(request.POST)

        if form.is_valid():

            username= form.cleaned_data["username"]

            form.save()

            return render(request, "AppCovid/inicio.html" ,{"mensaje": f"{username} Creado y Registrado"})

    else:
        form = UserRegisterForm()
        #form= UserCreationForm()
    return render(request, "AppCovid/register.html" , {"form": form})


@login_required
def editarPerfil(request):

    usuario= request.user

    if request.method == "POST":

        miFormulario = UserEditForm(request.POST)

        if miFormulario.is_valid():

            informacion= miFormulario.cleaned_data

            usuario.email= informacion["email"]
            usuario.password1= informacion["password1"]
            usuario.password2= informacion["password2"]

            usuario.save()

            return render(request, "AppCovid/inicio.html")

    else:

        miFormulario= UserEditForm(inicio=({"email": usuario.email}))

    return render(request, "AppCovid/editarPerfil.html", {"miFormulario": miFormulario, "usuario": usuario})
