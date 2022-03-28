from django.db import models


# Create your models here.
class Professor(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    ave_rate = models.IntegerField(default=0, verbose_name='avrage rate')
    rate_amount = models.IntegerField(default=0)
    total_rate = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "professor"


class Module(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "module"


class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, null=True, on_delete=models.SET_NULL)
    year = models.IntegerField(default=0)
    semester = models.IntegerField(default=0)
    professor = models.ForeignKey(Professor, null=True, on_delete=models.SET_NULL)
    Professor2 = models.ForeignKey(Professor, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='PROFESSOR_2')
    ave_rate1 = models.IntegerField(default=0)
    total_rate1 = models.IntegerField(default=0)
    rate_amount1 = models.IntegerField(default=0)
    ave_rate2 = models.IntegerField(default=0)
    total_rate2 = models.IntegerField(default=0)
    rate_amount2 = models.IntegerField(default=0)

    def __str__(self):
        return str(self.module.name + str(self.year) + str(self.semester) + self.professor.name)
