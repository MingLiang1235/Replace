def to_u_or_b(obj,encoding='utf-8'):  # to_unicode_or_bust
	if isinstance(obj,basestring):
		if not isinstance(obj,unicode):
			obj = unicode(obj,encoding)
	return obj

