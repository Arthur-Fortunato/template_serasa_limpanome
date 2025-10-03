from django.db import models
# ESTOU FAZENDO DE UMA FORMA QUE SEPARE AS PARCELAS, OS ACORDOS E OS ERROS
# NÃO SEI SE VAI QUERER SALVAR A PARTE DE DESCONTOS E COMISÃO, MAS É BASICAMENTE A MESMA COISA, SÓ ADICIONAR OS CAMPOS E MUDAR NA VIEW DEPOIS 

class SerasaLimpaNomeDividas(models.Model):
    agreement_id                        = models.CharField(blank=True, null=True, db_column='agreement_id')
    transaction_id                      = models.CharField(blank=True, null=True, db_column='transaction_id')
    debt_id                             = models.CharField(blank=True, null=True, db_column='debt_id')
    contract_number                     = models.CharField(blank=True, null=True, db_column='contract_number')
    document                            = models.CharField(blank=True, null=True, db_column='document')
    wallet                              = models.CharField(blank=True, null=True, db_column='wallet')
    occurrence_date                     = models.CharField(blank=True, null=True, db_column='occurrence_date')
    debt_type                           = models.CharField(blank=True, null=True, db_column='debt_type')
    debt_value                          = models.DecimalField(blank=True, null=True, db_column='debt_value')
    agreement_value                     = models.DecimalField(blank=True, null=True, db_column='agreement_value')
    offer_value                         = models.DecimalField(blank=True, null=True, db_column='offer_value')
    offer_due_days_first_installment    = models.IntegerField(blank=True, null=True, db_column='offer_due_days_first_installment')
    max_installments                    = models.IntegerField(blank=True, null=True, db_column='max_installments')
    debt_orig_name                      = models.CharField(blank=True, null=True, db_column='debt_orig_name')
    debt_orig_document                  = models.CharField(blank=True, null=True, db_column='debt_orig_document')
    agreement_date                      = models.DateField(blank=True, null=True, db_column='agreement_date')
    created_at                          = models.DateTimeField(blank=True, null=True, db_column='created_at')
    deal_status                         = models.CharField(blank=True, null=True, db_column='deal_status')
    settlement_date                     = models.DateField(blank=True, null=True, db_column='settlement_date')

    class Meta:
        managed  = False
        db_table = "SUA TABELA DE DIVIDAS"
    
class SerasaLimpaNomeParcelas(models.Model):
    transaction_id          = models.CharField(blank=True, null=True, db_column='transaction_id')
    debt_id                 = models.CharField(blank=True, null=True, db_column='debt_id') 
    agreement_id            = models.CharField(blank=True, null=True, db_column='agreement_id')
    installment             = models.IntegerField(blank=True, null=True, db_column='installment')
    installment_value       = models.DecimalField(blank=True, null=True, db_column='installment_value')
    due_date                = models.DateField(blank=True, null=True, db_column='due_date')
    payment_limit_date      = models.DateField(blank=True, null=True, db_column='payment_limit_date')
    payment_date            = models.DateField(blank=True, null=True, db_column='payment_date')
    installment_status      = models.CharField(blank=True, null=True, db_column='installment_status')
    created_at              = models.DateTimeField(blank=True, null=True, db_column='created_at')
 
    class Meta:
        managed  = False
        db_table = "SUA TABELA DE PARCELAS"
        
class SerasaLimpaNomeErros(models.Model):
    transaction_id = models.CharField(blank=True, null=True, db_column='transaction_id')
    debt_id        = models.CharField(blank=True, null=True, db_column='debt_id')
    status         = models.IntegerField(blank=True, null=True, db_column='status')
    error_origin   = models.CharField(blank=True, null=True, db_column='error_origin')
    error_message  = models.CharField(blank=True, null=True, db_column='error_message')
    created_at     = models.DateTimeField(blank=True, null=True, db_column='created_at')
 
    class Meta:
        managed  = False
        db_table = "SUA TABELA DE ERROS"