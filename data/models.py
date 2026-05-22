from tortoise import fields, models


class Session(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=32, index=True)
    clock_in = fields.DatetimeField()
    clock_out = fields.DatetimeField(null=True)

    class Meta:
        table = "sessions"


class ClockOutReminder(models.Model):
    id = fields.IntField(pk=True)
    session = fields.OneToOneField(
        "models.Session",
        related_name="clock_out_reminder",
        on_delete=fields.CASCADE,
    )
    sent_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "clock_out_reminders"
