 #!/bin/bash
 dos2unix "$@"
 rename 's/.*([0-9]*)_([0-9]*)_([0-9]*).*/$3-$2-$1-ruptura/g' "$@"
