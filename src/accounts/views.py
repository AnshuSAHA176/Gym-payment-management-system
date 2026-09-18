from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken

from .models import User
from .serializer import RegisterSerializer,LoginSerializer
from members.models import Member
from payment.models import Payment
from django.db.models import Count ,Q ,Sum

from django.utils import timezone
from datetime import timedelta
from payment.serializer import PaymentSerializer
from members.serializer import MemberDashboardSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):

        serializer = LoginSerializer(data = request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh_token = RefreshToken.for_user(user)

        access_token= refresh_token.access_token
        
        return Response (
            {
            "access":str(access_token),
            "refresh":str(refresh_token)

        }
        )



class DashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.localdate()

        summary = Member.objects.aggregate(
            total_members=Count('member_id'),

            active_members=Count(
                'member_id',
                filter=Q(is_active=True)
            ),

            inactive_members=Count(
                'member_id',
                filter=Q(is_active=False)
            ),

            due_today=Count(
                'member_id',
                filter=Q(payment_due_date=today)
            ),

            overdue=Count(
                'member_id',
                filter=Q(payment_due_date__lt=today)
            ),

            upcoming_payments=Count(
                'member_id',
                filter=Q(
                    payment_due_date__gt=today,
                    payment_due_date__lte=today + timedelta(days=7)
                )
            ),
        )

        monthly_collection = Payment.objects.filter(
            status="PAID",
            payment_date__year=today.year,
            payment_date__month=today.month,
        ).aggregate(
            total=Sum("amount")
        )

        recent_payments = Payment.objects.order_by(
            "-payment_date"
        )[:4]

        overdue_members = Member.objects.filter(
            payment_due_date__lt=today
        ).order_by(
            "payment_due_date"
        )

        due_today_members = Member.objects.filter(
            payment_due_date=today
        )

        return Response({
            "summery": summary,

            "monthly_collection": monthly_collection["total"] or 0,

            "recent_payments": PaymentSerializer(
                recent_payments,
                many=True
            ).data,

            "overdue_members": MemberDashboardSerializer(
                overdue_members,
                many=True
            ).data,

            "due_today_members": MemberDashboardSerializer(
                due_today_members,
                many=True
            ).data,
        })


from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})