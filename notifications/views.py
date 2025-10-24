from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Review, Rating, Report
from .serializers import (
    ReviewSerializer, RatingSerializer, ReportSerializer
)


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    List and create reviews
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        topic_id = self.request.query_params.get('topic_id')
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
            
        return queryset.order_by('-created_at')


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class RatingListCreateView(generics.ListCreateAPIView):
    """
    List and create ratings
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        topic_id = self.request.query_params.get('topic_id')
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
            
        return queryset.order_by('-rated_at')


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a rating
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportListCreateView(generics.ListCreateAPIView):
    """
    List and create reports
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.order_by('-created_at')


class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a report
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_notification_dashboard(request):
    """
    Get notification dashboard data
    """
    user = request.user
    
    # Get recent reviews by user
    recent_reviews = Review.objects.filter(
        reviewer_id=user
    ).order_by('-created_at')[:5]
    
    # Get recent ratings by user
    recent_ratings = Rating.objects.filter(
        user_id=user
    ).order_by('-rated_at')[:5]
    
    # Get reports by user
    user_reports = Report.objects.filter(
        reported_by=user
    ).order_by('-created_at')[:5]
    
    dashboard_data = {
        'recent_reviews': ReviewSerializer(recent_reviews, many=True).data,
        'recent_ratings': RatingSerializer(recent_ratings, many=True).data,
        'user_reports': ReportSerializer(user_reports, many=True).data,
        'total_reviews': Review.objects.filter(reviewer_id=user).count(),
        'total_ratings': Rating.objects.filter(user_id=user).count(),
        'total_reports': Report.objects.filter(reported_by=user).count(),
    }
    
    return Response(dashboard_data, status=status.HTTP_200_OK)