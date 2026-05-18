from tortoise import fields, models


class Session(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=32, index=True)
    clock_in = fields.DatetimeField()
    clock_out = fields.DatetimeField(null=True)

    class Meta:
        table = "sessions"
