#!/bin/sh

TOPDIR=${TOPDIR:-$(git rev-parse --show-toplevel)}
SRCDIR=${SRCDIR:-$TOPDIR/src}
MANDIR=${MANDIR:-$TOPDIR/doc/man}

TELECHAIND=${TELECHAIND:-$SRCDIR/telechaind}
BITCOINCLI=${BITCOINCLI:-$SRCDIR/telecli}
BITCOINTX=${BITCOINTX:-$SRCDIR/telechain-tx}
BITCOINQT=${BITCOINQT:-$SRCDIR/qt/telechain-qt}

[ ! -x $TELECHAIND ] && echo "$TELECHAIND not found or not executable." && exit 1

# The autodetected version git tag can screw up manpage output a little bit
BTCVER=($($BITCOINCLI --version | head -n1 | awk -F'[ -]' '{ print $6, $7 }'))

# Create a footer file with copyright content.
# This gets autodetected fine for telechaind if --version-string is not set,
# but has different outcomes for telechain-qt and telecli.
echo "[COPYRIGHT]" > footer.h2m
$TELECHAIND --version | sed -n '1!p' >> footer.h2m

for cmd in $TELECHAIND $BITCOINCLI $BITCOINTX $BITCOINQT; do
  cmdname="${cmd##*/}"
  help2man -N --version-string=${BTCVER[0]} --include=footer.h2m -o ${MANDIR}/${cmdname}.1 ${cmd}
  sed -i "s/\\\-${BTCVER[1]}//g" ${MANDIR}/${cmdname}.1
done

rm -f footer.h2m
