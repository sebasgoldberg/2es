 #!/bin/bash
 /usr/bin/dos2unix $@
 /usr/bin/rename 's/.*([0-9]*)_([0-9]*)_([0-9]*).*/$3-$2-$1-ruptura/g' $@
