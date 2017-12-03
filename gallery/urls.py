from django.urls import path
import gallery.views


urlpatterns = [
    #Gallery views
    path('gallery/', gallery.views.gallery_index),
    path('gallery/gallery_data=<int:page>/', gallery.views.gallery_index_data),
    path('new_gallery/', gallery.views.edit_gallery),
    path('gallery=<int:gallery_id>/edit/', gallery.views.edit_gallery),
    path('gallery=<int:gallery_id>/delete/', gallery.views.delete_gallery),

    #Gallery Image views
    path('gallery=<int:gallery_id>/', gallery.views.gallery),
    path('gallery=<int:gallery_id>/image=<int:image_id>/', gallery.views.gallery),
    path('gallery=<int:gallery_id>/image_data=<int:page>/', gallery.views.gallery_images),
    path('gallery=<int:gallery_id>/upload_images/', gallery.views.upload_images),
    path('gallery=<int:gallery_id>/upload_images_post/', gallery.views.upload_images_post),

    #Image views
    path('image=<int:image_id>/details/', gallery.views.image_detail),
    path('image=<int:image_id>/update/', gallery.views.image_detail_update),
    path('image=<int:image_id>/delete/', gallery.views.image_delete),
    path('image=<int:image_id>/make_gallery_thumbnail/', gallery.views.set_image_as_gallery_thumbnail),
    path('image=<int:image_id>/rotate/', gallery.views.rotate_image),

    #Tagging API
    path('image=<int:image_id>/tags/get/', gallery.views.get_tags),
    path('tag=<int:tag_id>/delete/', gallery.views.delete_tag),
    path('image=<int:image_id>/tags/create/', gallery.views.create_tag),

    #Person Gallery Views
    path('person=<int:person_id>/photos/', gallery.views.person_gallery),
    path('person=<int:person_id>/photos/image=<int:image_id>/', gallery.views.person_gallery),
    path('person=<int:person_id>/photos/image_data=<int:page>/', gallery.views.person_gallery_data),

    #Gallery Map Views
    path('gallery=<int:gallery_id>/map/', gallery.views.gallery_map),
    path('gallery=<int:gallery_id>/map_data/', gallery.views.gallery_map_data),
    path('image=<int:image_id>/address/', gallery.views.geocode_image_location_post),
]
