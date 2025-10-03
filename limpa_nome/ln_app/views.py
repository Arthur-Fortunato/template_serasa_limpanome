import json
from datetime import datetime
from dateutil import parser
from django.shortcuts import render
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
    evento = payload.get("eventType")
    if evento != "DebtCreatedEvent":
        return JsonResponse({"message": "Evento não suportado"}, status=400)
    
    oferta       = payload.get("offer", {}) or {}
    debt_orig    = payload.get("debtOrigin", {}) or {}
    error        = payload.get("errors", []) or payload.get("error", []) or []
    if error:
        SerasaLimpaNomeErros.objects.create(
            transaction_id = payload.get("transactionId"),
            debt_id        = payload.get("debtId"),
            status         = payload.get("status"),
            error_origin   = error[0].get("origin"),
            error_message  = error[0].get("message"),
            created_at     = payload.get("createdAt") 
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
    
@csrf_exempt
def hook_acordo_efetivado(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")
    try: 
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"message": "JSON inválido"}, status=400)
    evento = payload.get("eventType")
    if evento != "ClosedAgreementEvent":
        return JsonResponse({"message": "Evento não suportado"}, status=400)
    
    agreement_id   = payload.get("agreementId")
    debt_ids       = payload.get("debtIds", [])
    created_at_str = payload.get("createdAt")
    data_acordo    = payload.get("agreementDate")
    parcelas       = payload.get("installments", []) 
    status         = "Efetivado"
    
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

        acordo.agreement_id    = agreement_id
        acordo.created_at      = created_at
        acordo.agreement_date  = agreement_date_parsed
        acordo.agreement_value = payload.get("agreementValue")
        acordo.deal_status     = status   
        acordo.save()

        for parcela in parcelas:
            numero = parcela.get("number")                
            SerasaLimpaNomeParcelas.objects.update_or_create(
                transaction_id        = acordo.transaction_id,
                debt_id               = acordo.debt_id,
                installment           = numero,
                defaults={
                    "installment_value"     : float(parcela.get("value")),
                    "due_date"              : datetime.strptime(parcela.get("dueDate"), "%Y-%m-%d").date(),
                    "payment_limit_date"    : datetime.strptime(parcela.get("paymentLimitDate"), "%Y-%m-%d").date(),
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
    if payload.get("eventType") != "BreachedAgreementEvent":
        return JsonResponse({"message": "Evento não suportado"}, status=400)
    
    created_at_str = payload.get("createdAt")
    try:
        created_at = datetime.fromisoformat(created_at_str.replate(" ", "T"))
    except:
        created_at = None
        
    debt_ids = payload.get("debtIds", [])
    for debt_id in debt_ids:
        SerasaLimpaNomeDividas.objects.filter(
            debt_id = debt_id
        ).update(
            created_at          = created_at,
            agreement_id        = payload.get("agreementId")
        )