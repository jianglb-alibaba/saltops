import rediscache_manager

def post_list(request):
    """ËùÓÐÒÑ·¢²¼ÎÄÕÂ"""
    posts = Post.objects.annotate(num_comment=Count('comment')).filter(
        published_date__isnull=False).prefetch_related(
        'category').prefetch_related('tags').order_by('-published_date')
    for p in posts:
        p.click = rediscache_manager.get_click(p)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    try:
        pass
    except:
        raise Http404()
    if post.published_date:
        rediscache_manager.update_click(post)
        post.click = rediscache_manager.get_click(post)