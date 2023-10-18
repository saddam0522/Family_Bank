from django import forms
from .models import Transactions


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['amount','transaction_type']
        
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disable = True
        self.fields['transaction_type'].widget= forms.HiddenInput()
        
    def save(self,commit = True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )
        return amount
    
class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        balance = account.balance
        max_withdraw_amount = balance-500
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You need to withdraw at least {min_withdraw_amount} $'
            )
            
        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} $ in your account.'
                'You can not withdraw more than your account balance '
            )
            
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can Withdraw at MOST {max_withdraw_amount} $'
            ) 
            
        return amount
    
    
class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        balance = account.balance
        max_loan_amount = 2 * balance
        amount = self.cleaned_data.get('amount')
        if amount > max_loan_amount:
            raise forms.ValidationError(
                f'You can request a Loan amount of double of your balace '
            )
        return amount
    
        
        