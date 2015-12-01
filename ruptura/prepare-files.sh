 #!/bin/bash
 /usr/bin/dos2unix $@
 /usr/bin/rename 's/(.*)\/.*_([0-9]*)_([0-9]*)_([0-9]*).*/$1\/$4-$3-$2-ruptura/g' $@
