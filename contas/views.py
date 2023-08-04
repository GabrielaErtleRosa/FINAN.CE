from django.shortcuts import render, redirect
from perfil.models import Categoria
from .models import ContaPagar, ContaPaga
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime

# Create your views here.

def definir_contas(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html',{'categorias': categorias})
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = ContaPagar(
            titulo = titulo,
            categoria_id = categoria, #pq ta recebendo id 
            descricao = descricao,
            valor = valor,
            dia_pagamento = dia_pagamento
        )

        conta.save()

        messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')

        return redirect('/contas/definir_contas')
    

def ver_contas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month = MES_ATUAL).values('conta') #lista das pagas(lista de id)
    #usar variável contas pra nao acessar o bd mtas vezes(da pra filtrar)
    contas_vencidas = contas.filter(dia_pagamento__lt = DIA_ATUAL).exclude(id__in= contas_pagas) #lista das vencidas menos as pagas
    # __lte quer dizer menor ou igual
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = (DIA_ATUAL + 5)).filter(dia_pagamento__gt=DIA_ATUAL).exclude(id__in= contas_pagas)
    
    #numeros pra home

    numero_contas_vencidas = len(list(contas_vencidas))
    numero_contas_proximas_vencimento = len(list(contas_proximas_vencimento))
    #
    #print(numero_contas_proximas_vencimento)
    #print(numero_contas_vencidas)

    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in= contas_proximas_vencimento).exclude(id__in=contas_pagas)

    return render(request, 'ver_contas.html', {'contas_vencidas': contas_vencidas, 'contas_proximas_vencimento': contas_proximas_vencimento , 'restantes': restantes, 'numero_contas_proximas_vencimento':numero_contas_proximas_vencimento })


