git remote set-url other git@github.com:EUye9IM/${1}.git && \
	git fetch other && \
	git checkout other && \
	git reset --hard other/${2} \
	&& f=`mktemp -d` && \
	mv `ls -a -I. -I.. -I.git` $f && \
	mv $f ${1} && git add . && \
	git commit -m "[REF] move" && \
	git checkout main && \
	git merge --allow-unrelated-histories other -m "merge" && \
	git push