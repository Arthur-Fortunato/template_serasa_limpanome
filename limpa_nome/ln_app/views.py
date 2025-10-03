import json
from datetime import datetime
from dateutil import parser
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseNotAllowed, JsonResponse
from .models import SerasaLimpaNomeDividas, SerasaLimpaNomeParcelas, SerasaLimpaNomeErros

@csrf_exempt
def hook_inclusao(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")
    try: 
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"message": "JSON inválido"}, status=400)
    event = payload.get("eventType")
    if event != "DebtCreatedEvent":
        return JsonResponse({"message": "Evento não suportado"}, status=400)
    
    oferta        = payload.get("offer", {}) or {}
    debt_orig     = payload.get("debtOrigin", {}) or {}
    errors        = payload.get("errors", []) or payload.get("error", []) or []
    create_at_str = payload.get("createdAt")
    if create_at_str:
        create_at = datetime.fromisoformat(create_at_str.replace(" ", "T")) if create_at_str else None
    else:
        create_at = None
            
    if error:
        for error in errors:
            SerasaLimpaNomeErros.objects.create(
                transaction_id = payload.get("transactionId"),
                debt_id        = payload.get("debtId"),
                status         = payload.get("status"),
                error_origin   = error.get("origin"),
                error_message  = error.get("message"),
                created_at     = create_at,
                error_event    = "Inclusion" 
            )
    if oferta == {}:
        SerasaLimpaNomeDividas.objects.create(
            transaction_id      = payload.get("transactionId"),
            debt_id             = payload.get("debtId"),
            contract_number     = payload.get("contractNumber"),
            document            = payload.get("document"),
            wallet              = payload.get("wallet"),
            occurrence_date     = payload.get("occurrenceDate"),
            debt_type           = payload.get("debtType"),
            debt_value          = payload.get("debtValue"),
            created_at          = payload.get("createdAt"),
            debt_orig_name      = debt_orig.get("name"),
            debt_orig_document  = debt_orig.get("document")
        )
    else:
        SerasaLimpaNomeDividas.objects.create(
            transaction_id                      = payload.get("transactionId"),
            debt_id                             = payload.get("debtId"),
            contract_number                     = payload.get("contractNumber"),
            document                            = payload.get("document"),
            wallet                              = payload.get("wallet"),
            occurrence_date                     = payload.get("occurrenceDate"),
            debt_type                           = payload.get("debtType"),
            debt_value                          = payload.get("debtValue"),
            offer_value                         = oferta.get("value"),
            offer_due_days_first_installment    = oferta.get("dueDaysFirstInstallment"),
            max_installments                    = oferta.get("maxInstallments"),
            debt_orig_name                      = debt_orig.get("name"),
            debt_orig_document                  = debt_orig.get("document"),
            created_at                          = payload.get("createdAt")
        )
    return JsonResponse({"message": "DebtCreated processado."}, status=200)
    
@csrf_exempt    
def hook_exclusao(request):
    if request.method != "POST":
        return JsonResponse({"message": "Método não permitido"}, status=400)
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"message": "JSON inválido"}, status=200)
    event = payload.get("eventType")
    if event != "DebtRemovedEvent":
        return JsonResponse({"message": "Evento não suportado"}, status=400)

    errors         = payload.get("error", []) or payload.get("errors", []) or []
    debt_id        = payload.get("debtId")
    transaction_id = payload.get("transaction_id")
    created_at_str = payload.get("createdAt")
    try:
        created_at = datetime.fromisoformat(created_at_str.replace(" ", "T")) if created_at_str else None
    except:
        created_at = None
        
    if errors:
        for error in errors:
            SerasaLimpaNomeErros.objects.create(
                transaction_id = transaction_id,
                debt_id        = debt_id,
                status         = payload.get("status"),
                error_origin   = error.get("origin"),
                error_message  = error.get("message"),
                created_at     = created_at,
                error_event    = "Exclusion"
            )
    else:
        SerasaLimpaNomeDividas.objects.filter(
            transaction_id = transaction_id,
            debt_id        = debt_id
        ).update(
            agreement_status = "Removed",
            exclusion_date   = datetime.date().today()
        )
        
        # AQUI PODE DECIDIR DE VAI DELETAR TODAS AS PARCELAS DO BANCO OU SE VAI DEIXAR LÁ MESMO
        
    
@csrf_exempt
def hook_acordo_efetivado(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")
    try: 
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"message": "JSON inválido"}, status=400)
    event = payload.get("eventType")
    if event != "ClosedAgreementEvent":
        return JsonResponse({"message": "Evento não suportado"}, status=400)
    
    agreement_id        = payload.get("agreementId")
    debt_ids            = payload.get("debtIds", [])
    created_at_str      = payload.get("createdAt")
    data_acordo         = payload.get("agreementDate")
    parcelas            = payload.get("installments", []) 
    agreement_status    = "Effectivated"
    
    for debt_id in debt_ids:
        try:
            acordo                  = SerasaLimpaNomeDividas.objects.get(debt_id=debt_id)
            agreement_date_parsed   = parser.isoparse(data_acordo).date() if data_acordo else None
        except SerasaLimpaNomeDividas.DoesNotExist:
            return JsonResponse({"message": "Acordo não encontrado"}, status=404)
        
        try:
            created_at = datetime.fromisoformat(created_at_str.replace(" ", "T")) if created_at_str else None
        except Exception:
            created_at = None

        acordo.agreement_id     = agreement_id
        acordo.created_at       = created_at
        acordo.agreement_date   = agreement_date_parsed
        acordo.agreement_value  = payload.get("agreementValue")
        acordo.agreement_status = agreement_status   
        acordo.save()

        for parcela in parcelas:
            number = parcela.get("number")                
            if number == 1:
                installment_status = "Ongoing"
            else:
                installment_status = "Unavailable"
            SerasaLimpaNomeParcelas.objects.update_or_create(
                transaction_id        = acordo.transaction_id,
                debt_id               = acordo.debt_id,
                installment           = number,
                defaults={
                    "installment_value"     : float(parcela.get("value")),
                    "due_date"              : datetime.strptime(parcela.get("dueDate"), "%Y-%m-%d").date(),
                    "payment_limit_date"    : datetime.strptime(parcela.get("paymentLimitDate"), "%Y-%m-%d").date(),
                    "installment_status"    : installment_status,
                    "created_at"            : created_at,
                    "agreement_id"          : agreement_id
                }
            )

    return JsonResponse({"message": "ClosedAgreement processado."}, status=200)

def hook_acordo_quebrado(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"message": "JSON inválido"}, status=400)
    event = payload.get("eventType")
    if  event != "BreachedAgreementEvent":
        return JsonResponse({"message": "Evento não suportado"}, status=400)
    
    created_at_str = payload.get("createdAt")
    try:
        created_at = datetime.fromisoformat(created_at_str.replate(" ", "T"))
    except:
        created_at = None
        
    agreement_status = "Broken"
        
    debt_ids = payload.get("debtIds", [])
    for debt_id in debt_ids:
        SerasaLimpaNomeDividas.objects.filter(
            debt_id = debt_id
        ).update(
            agreement_status   = agreement_status,      
            created_at         = created_at,
            agreement_id       = payload.get("agreementId")
        )
        
        SerasaLimpaNomeParcelas.objects.filter(
            debt_id = debt_id
        ).update(
            installment_status = agreement_status
        )
    return JsonResponse({"message": "BreachedAgreement processado."}, status=200)
        
def hook_acordo_quitado(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"message": "JSON inválido"}, status=400)
    event = payload.get("eventType")
    if event != "PaidAgreementEvent":
        return JsonResponse({"message": "Evento não suportado"}, status=400)
    
    debt_ids            = payload.get("debtIds", [])
    settlement_date_str = payload.get("date")
    settlement_date     = parser.isoparse(settlement_date_str).date() if settlement_date_str else None
    agreement_status    = "Paid"
    
    created_at_str = payload.get("createdAt")
    try:
        created_at = datetime.fromisoformat(created_at_str.replate(" ", "T"))
    except:
        created_at = None
    
    for debt_id in debt_ids:
        SerasaLimpaNomeDividas.objects.filter(
            debt_id = debt_id
        ).update(
            agreement_status = agreement_status,
            settlement_date  = settlement_date,
            agreement_id     = payload.get("agreementId"),
            created_at       = created_at
        )
    return JsonResponse({"message": "PaidAgreement processado."}, status=200)

def hook_pagamento_parcela(request):
    if request.method != "POST":
        return JsonResponse({"message": "Método não permitido"}, status=400)
    try:
        payload = json.loads(request.body)
    except:
        return JsonResponse({"message": "JSON inválido"}, status=400)
    event = payload.get("eventType")
    if event != "PaidInstallmentEvent":
        return JsonResponse({"message": "Evento não suportado"}, status=400)
    
    installment      = payload.get("installmentNumber")
    payment_date     = payload.get("paymentDate")
    debt_ids         = payload.get("debtIds", [])
    agreement_id     = payload.get("agreementId")
    next_installment = int(installment) + 1  
    
    for debt_id in debt_ids:
        inst = SerasaLimpaNomeParcelas.objects.filter(
            debt_id     = debt_id,
            installment = installment
        ).first()
        
        if inst:
            inst.agreement_id       = agreement_id
            inst.payment_date       = payment_date
            inst.installment_status = "Paid"
            inst.save()
        
            next_inst = SerasaLimpaNomeParcelas.objects.filter(
                transaction_id = inst.transaction_id,
                installment    = next_installment
            ).first()
            
            if next_inst:
                next_inst.installment_status = "Ongoing"
                next_inst.save()
                
    return JsonResponse({"message": "PaidInstallment processado."}, status=200)

