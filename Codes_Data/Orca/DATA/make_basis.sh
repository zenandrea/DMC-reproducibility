basis='cc-pVTZ'
for i in H C O
do
echo $i
cat /Users/zen/GitHub_local/DMC-codes-comparison/pseudopotentials/${i}.${basis}.gamess \
| sed 's/s/S/g' \
| sed 's/p/P/g' \
| sed 's/d/D/g' \
| sed 's/f/F/g' \
| sed 's/g/G/g' \
| sed 's/h/H/g' \
| awk '{ if ($1=="S" || $1=="P" || $1=="D" || $1=="F" || $1=="G" || $1=="H") print $1, $2; else print; }' 
done > BASISSET

