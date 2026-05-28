from django.urls import path,include
from app_module.admin_app import views

app_name = 'admin_app' 

urlpatterns = [

    path('',views.index,name='index'),
    path('components_alerts/',views.components_alerts,name='components_alerts'),
    path('components_accordion/',views.components_accordion,name='components_accordion'),
    path('components_badges/',views.components_badges,name='components_badges'),
    path('components_breadcrumbs/',views.components_breadcrumbs,name='components_breadcrumbs'),
    path('components_buttons/',views.components_buttons,name='components_buttons'),
    path('components_cards/',views.components_cards,name='components_cards'),
    path('components_carousel/',views.components_carousel,name='components_carousel'),
    path('components_list_group/',views.components_list_group,name='components_list_group'),
    path('components_modal/',views.components_modal,name='components_modal'),
    path('components_pagination/',views.components_pagination,name='components_pagination'),
    path('components_progress/',views.components_progress,name='components_progress'),
    path('components_spinners/',views.components_spinners,name='components_spinners'),
    path('components_tabs/',views.components_tabs,name='components_tabs'),
    path('components_tooltips/',views.components_tooltips,name='components_tooltips'),

    path('forms_editors/',views.forms_editors,name='forms_editors'),
    path('forms_elements/',views.forms_elements,name='forms_elements'),
    path('forms_layouts/',views.forms_layouts,name='forms_layouts'),
    path('forms_validation/',views.forms_validation,name='forms_validation'),

    path('tables_data/',views.tables_data,name='tables_data'),
    path('tables_general/',views.tables_general,name='tables_general'),

    path('charts_chartjs/',views.charts_chartjs,name='charts_chartjs'),
    path('charts_apexcharts/',views.charts_apexcharts,name='charts_apexcharts'),
    path('charts_echarts/',views.charts_echarts,name='charts_echarts'),

    path('icons_bootstrap/',views.icons_bootstrap,name='icons_bootstrap'),
    path('icons_boxicons/',views.icons_boxicons,name='icons_boxicons'),
    path('icons_remix/',views.icons_remix,name='icons_remix'),

    path('users_profile/',views.users_profile,name='users_profile'),
    path('pages_faq/',views.pages_faq,name='pages_faq'),
    path('pages_contact/',views.pages_contact,name='pages_contact'),
    path('pages_error_fzf/',views.pages_error_fzf,name='pages_error_fzf'),
    path('pages_blank/',views.pages_blank,name='pages_blank'),

    # path('pages_register/',views.pages_register,name='pages_register'),
    # path('pages_login/',views.pages_login,name='pages_login'),
    # path('logout_view/',views.logout_view,name='logout_view'),

    path('comments_list_view/',views.comments_list_view,name='comments_list_view'),
    path('contect_list_view/',views.contect_list_view,name='contect_list_view'),
    path('subscribe_list_view/',views.subscribe_list_view,name='subscribe_list_view'),

    path('add_category_view/',views.add_category_view,name='add_category_view'),
    path('list_category_view/',views.list_category_view,name='list_category_view'),
    path('update_category_view/<int:id>/',views.update_category_view,name='update_category_view'),
    path('delete_category_view/<int:id>/',views.delete_category_view,name='delete_category_view'),

    path('add_product_view/',views.add_product_view,name='add_product_view'),
    path('list_product_view/',views.list_product_view,name='list_product_view'),
    path('update_product_view/<int:id>/',views.update_product_view,name='update_product_view'),
    path('delete_product_view/<int:id>/',views.delete_product_view,name='delete_product_view'),

    path('user_list_view/',views.user_list_view,name='user_list_view'),

    path('block_user_view/<int:id>/',views.block_user_view,name='block_user_view'),
    path('unblock_user_view/<int:id>/',views.unblock_user_view,name='unblock_user_view'),
    
    path('order_list_view/',views.order_list_view,name='order_list_view'),
    path('payment_list_view/',views.payment_list_view,name='payment_list_view'),
    path('order_detail_view/<int:id>/',views.order_detail_view,name='order_detail_view'),
    path('update_order_status/<int:id>/',views.update_order_status,name='update_order_status'),

    path('review_list_view/',views.review_list_view,name='review_list_view'),
    path('delete_review_view/<int:id>/',views.delete_review_view,name='delete_review_view'),

    path('notification_list_view/',views.notification_list_view,name='notification_list_view'),
    path('mark_notification_read/<int:id>/',views.mark_notification_read,name='mark_notification_read'),
    path('quick_update_payment_status/<int:id>/',views.quick_update_payment_status,name='quick_update_payment_status'),

]
