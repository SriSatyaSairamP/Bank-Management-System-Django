from django.db import models
from django.core.validators import RegexValidator,MinLengthValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Bank(models.Model):

    bank_name= models.CharField(
        max_length=100,
        unique =True,
        validators = [
            RegexValidator(
                regex= r'^[A-Za-z ]+$',
                message = "Bank name must contain only alphabets and spaces."
            )
        ]
        )
    bank_code = models.CharField(
        max_length =4,
        unique=True,
        validators = [
            RegexValidator(
                regex = r'^[A-Z]{4}$',
                message = "Bank code must contain exactly 4 uppercase letters."
                )
                ]
    )
    head_office = models.CharField(max_length=255)
    customer_care_number=models.CharField(max_length =15,unique=True)
    email = models.EmailField(unique=True)
    website = models.URLField(unique=True)

    is_active =models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.bank_name}({self.bank_code})"


class Branch(models.Model):

    bank = models.ForeignKey(
        Bank,
        on_delete = models.PROTECT,
        related_name= "branches"
    )

    branch_name = models.CharField(max_length=100,unique =True)

    branch_code =models. CharField(
        max_length = 4,
        unique = True,
        validators = [
            RegexValidator(
                regex=r'^\d{4}$',
                message = "Branch code must contain exactly 4 digits."
            )
        ]
    )

    ifsc_code = models.CharField(
        max_length =11,
        unique =True,
        editable=False
    )

    def save(self,*args,**kwargs):
        six_digit_branch_code = self.branch_code.zfill(6)
        self.ifsc_code = f"{self.bank.bank_code}0{six_digit_branch_code}"
        super().save(*args,**kwargs)


    address = models.CharField(max_length =255)
    city = models .CharField(max_length=100)
    state  = models.CharField(max_length=100)

    pin_code = models.CharField(
        max_length=6,
        validators= [
            RegexValidator(
                regex = r'^\d{6}$',
                message = "PIN code must contain exactly 6 digits."
            )
        ]
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "branches"
        ordering = ["bank", "branch_name"]
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

        constraints = [
            models.UniqueConstraint(
                fields=["bank", "branch_name"],
                name="unique_branch_name_per_bank"
            ),
            models.UniqueConstraint(
                fields=["bank", "branch_code"],
                name="unique_branch_code_per_bank"
            ),
        ]

    def __str__(self):
        return (
            f"{self.branch_name} - "f"{self.bank.bank_name} ({self.ifsc_code})"
        )



class CustomerApplication(models.Model):

    branch = models.ForeignKey(
        Branch,
        on_delete =models.PROTECT,
        null=True,
        blank=True,
        related_name = "applications"
    )
    
    application_id = models.CharField(max_length=12,unique=True,editable = False)
    
    def save(self,*args,**kwargs):        
              
        if not self.application_id:
            today = timezone.localdate()
            date_prefix = today.strftime("%Y%m%d")

            last_application = self.__class__.objects.filter(
                application_id__startswith=date_prefix
            ).order_by("-application_id").first()

            if last_application:
                last_sequence = int(last_application.application_id[-4:])
                new_sequence = last_sequence+1
            else:
                new_sequence=1
            self.application_id = f"{date_prefix}{new_sequence:04d}"

        branch=Branch.objects.get(
            pin_code = self.current_pin_code)
        if branch:
            self.branch = branch
        else:
            raise ValidationError(
                "No branch found for the entered PIN."
            )
        super().save(*args,**kwargs)

            
    full_name = models.CharField(max_length=100,
                                 validators = [
                                     RegexValidator(
                                         regex = r'^[A-Za-z ]+$',
                                         message="Full name must contain only alphabets and spaces."
                                     )
                                 ])
    date_of_birth =models.DateField()
    mobile_number= models.CharField(max_length=10,
                                    validators=[
                                        MinLengthValidator(10),
                                        RegexValidator(
                                            regex=r'^\d{10}$',
                                            message="Mobile number must contain exactly 10 digits."
                                        )
                                    ]
                            )
    email = models.EmailField(blank=True,null=True)
    identity_proof_type = models.CharField(max_length=50)
    identity_id = models.CharField(max_length=12,unique=True,
                validators= [
                    
                    RegexValidator(
                        regex =r'^\d{12}$',
                        message = "Identity ID must contain exactly 16 digits."
                    )
                ])
    # identity_document = models.FileField(...)
    permanent_address = models.CharField(max_length=255)
    permanent_city = models.CharField(max_length=100)
    permanent_state=models.CharField(max_length=100)

    permanent_pin_code= models.CharField(max_length=6,
                                         validators = [
                                             RegexValidator(
                                                 regex = r'^\d{6}$',

                                                 message = "PIN code must contain exactly 6 digits."
                                             )
                                         ])
    
    current_address = models.CharField(max_length=255, blank=True)
    current_city =models.CharField(max_length=100,blank=True)
    current_state = models.CharField(max_length=100,blank=True)
    current_pin_code = models.CharField(max_length=6,
                                        blank=True,
                                        validators=[
                                            RegexValidator(
                                                regex= r"^\d{6}$",
                                                message = "PIN code must contain exactly 6 digits."
                                            )
                                        ])
    
    address_proof_type =  models.CharField(max_length=50)

    status = models.CharField(
        max_length=10,
        choices=[
            ("PENDING","Pending"),
            ("APPROVED","Approved"),
            ("REJECTED","Rejected"),
        ],
        default="PENDING"
    )

    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table =  "applications"
        ordering = ["status", "-created_at"]
        verbose_name = "Application"
        verbose_name_plural="Applications"

    
    def __str__(self):
        return (
            f"{self.full_name}"
        )
    

class Customer(models.Model):
    application = models.OneToOneField(
        CustomerApplication,on_delete=models.PROTECT,
        related_name="customer"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="customers"
    )
    customer_id = models.CharField(max_length=14,
                                   unique=True,
                                   editable=False)


    def save(self,*args,**kwargs):

        if not self.customer_id:
            bank_code = self.branch.bank.bank_code
            branch_code = self.branch.branch_code

            last_customer= (
                            self.__class__.objects.filter(branch=self.branch)
                            .order_by("-customer_id").first()
            )

            if last_customer:
                last_sequence = int(last_customer.customer_id[-6:])
                new_sequence =last_sequence+1

            else:
                new_sequence = 1
                        
            self.customer_id = f"{bank_code}{branch_code}{new_sequence:06d}"        

        super().save(*args, **kwargs)

    class Meta:

        db_table = "customer"
        ordering = ["customer_id"]
        verbose_name = "Customer"
        verbose_name_plural = "customers"

    def __str__(self):
        return f"{self.customer_id} - {self.application.full_name}"