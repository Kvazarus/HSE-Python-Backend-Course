def filter_comments_by_author(comments, author):
    return list(filter((lambda comment: comment.author_id == author.id), comments))
