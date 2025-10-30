import sqlite3
import os
import re

# Tên database
DB_NAME = "dictionary.db"

RAW_PHIEN_AM_DATA = """
abandon    /əˈbændən/
ability    /əˈbɪləti/
able       /ˈeɪbəl/
about      /əˈbaʊt/
above      /əˈbʌv/
abroad     /əˈbrɔːd/
absence    /ˈæbsəns/
absolute   /ˈæbsəluːt/
absorb     /əbˈzɔːb/
academic   /ˌækəˈdemɪk/
accept     /əkˈsept/
access     /ˈækses/
accident   /ˈæksɪdənt/
accompany  /əˈkʌmpəni/
according  /əˈkɔːdɪŋ/
account    /əˈkaʊnt/
accurate   /ˈækjərət/
accuse     /əˈkjuːz/
achieve    /əˈtʃiːv/
acquire    /əˈkwaɪə/
across     /əˈkrɒs/
act        /ækt/
action     /ˈækʃən/
active     /ˈæktɪv/
activity   /ækˈtɪvɪti/
actor      /ˈæktə/
actress    /ˈæktrəs/
actual     /ˈæktʃuəl/
actually   /ˈæktʃuəli/
add        /æd/
addition   /əˈdɪʃən/
additional /əˈdɪʃənəl/
address    /əˈdres/
administration /ədˌmɪnɪˈstreɪʃən/
admire     /ədˈmaɪə/
admit      /ədˈmɪt/
adult      /ˈædʌlt/
advance    /ədˈvɑːns/
advantage  /ədˈvɑːntɪdʒ/
adventure  /ədˈventʃə/
advertise  /ˈædvətaɪz/
advice     /ədˈvaɪs/
advise     /ədˈvaɪz/
affair     /əˈfeə/
affect     /əˈfekt/
afford     /əˈfɔːd/
afraid     /əˈfreɪd/
after      /ˈɑːftə/
afternoon  /ˌɑːftəˈnuːn/
again      /əˈɡen/
against    /əˈɡenst/
age        /eɪdʒ/
agency     /ˈeɪdʒənsi/
agent      /ˈeɪdʒənt/
ago        /əˈɡəʊ/
agree      /əˈɡriː/
agreement  /əˈɡriːmənt/
ahead      /əˈhed/
aid        /eɪd/
aim        /eɪm/
air        /eə/
aircraft   /ˈeəkrɑːft/
airport    /ˈeəpɔːt/
alarm      /əˈlɑːm/
album      /ˈælbəm/
alcohol    /ˈælkəhɒl/
alive      /əˈlaɪv/
all        /ɔːl/
allow      /əˈlaʊ/
almost     /ˈɔːlməʊst/
alone      /əˈləʊn/
along      /əˈlɒŋ/
already    /ɔːlˈredi/
also       /ˈɔːlsəʊ/
although   /ɔːlˈðəʊ/
always     /ˈɔːlweɪz/
amazing    /əˈmeɪzɪŋ/
ambition   /æmˈbɪʃən/
amount     /əˈmaʊnt/
analyse    /ˈænəlaɪz/
analysis   /əˈnæləsɪs/
ancient    /ˈeɪnʃənt/
anger      /ˈæŋɡə/
angle      /ˈæŋɡəl/
angry      /ˈæŋɡri/
animal     /ˈænɪməl/
announce   /əˈnaʊns/
annual     /ˈænjuəl/
another    /əˈnʌðə/
answer     /ˈɑːnsə/
anxiety    /æŋˈzaɪəti/
any        /ˈeni/
anybody    /ˈenibɒdi/
anymore    /ˌeniˈmɔː/
anyone     /ˈeniwʌn/
anything   /ˈeniθɪŋ/
anyway     /ˈeniweɪ/
apart      /əˈpɑːt/
apartment  /əˈpɑːtmənt/
apologise  /əˈpɒlədʒaɪz/
apparent   /əˈpærənt/
appeal    /əˈpiːl/
appear    /əˈpɪə/
appearance    /əˈpɪərəns/
application    /ˌæplɪˈkeɪʃən/
apply    /əˈplaɪ/
appoint    /əˈpɔɪnt/
appointment    /əˈpɔɪntmənt/
appreciate    /əˈpriːʃieɪt/
approach    /əˈprəʊtʃ/
appropriate    /əˈprəʊpriət/
approval    /əˈpruːvəl/
approve    /əˈpruːv/
area    /ˈeəriə/
argue    /ˈɑːɡjuː/
argument    /ˈɑːɡjʊmənt/
arise    /əˈraɪz/
arm    /ɑːm/
armed    /ɑːmd/
army    /ˈɑːmi/
around    /əˈraʊnd/
arrange    /əˈreɪndʒ/
arrangement    /əˈreɪndʒmənt/
arrest    /əˈrest/
arrival    /əˈraɪvəl/
arrive    /əˈraɪv/
art    /ɑːt/
article    /ˈɑːtɪkəl/
artist    /ˈɑːtɪst/
artistic    /ɑːˈtɪstɪk/
as    /æz/
ashamed    /əˈʃeɪmd/
ask    /ɑːsk/
asleep    /əˈsliːp/
aspect    /ˈæspekt/
assist    /əˈsɪst/
assistance    /əˈsɪstəns/
associate    /əˈsəʊʃieɪt/
association    /əˌsəʊʃiˈeɪʃən/
assume    /əˈsjuːm/
atmosphere    /ˈætməsfɪə/
attach    /əˈtætʃ/
attack    /əˈtæk/
attempt    /əˈtempt/
attend    /əˈtend/
attention    /əˈtenʃən/
attitude    /ˈætɪtjuːd/
attract    /əˈtrækt/
attraction    /əˈtrækʃən/
attractive    /əˈtræktɪv/
audience    /ˈɔːdiəns/
author    /ˈɔːθə/
authority    /ɔːˈθɒrɪti/
available    /əˈveɪləbl/
average    /ˈævərɪdʒ/
avoid    /əˈvɔɪd/
award    /əˈwɔːd/
aware    /əˈweə/
away    /əˈweɪ/
awful    /ˈɔːfəl/
baby    /ˈbeɪbi/
back    /bæk/
background    /ˈbækgraʊnd/
bad    /bæd/
badly    /ˈbædli/
bag    /bæɡ/
bake    /beɪk/
balance    /ˈbæləns/
ball    /bɔːl/
ban    /bæn/
band    /bænd/
bank    /bæŋk/
bar    /bɑː/
base    /beɪs/
basic    /ˈbeɪsɪk/
basis    /ˈbeɪsɪs/
bath    /bɑːθ/
bathroom    /ˈbɑːθruːm/
battery    /ˈbætəri/
battle    /ˈbætl/
be    /biː/
beach    /biːtʃ/
bean    /biːn/
bear    /beə/
beat    /biːt/
beautiful    /ˈbjuːtɪfəl/
beauty    /ˈbjuːti/
because    /bɪˈkɒz/
become    /bɪˈkʌm/
bed    /bed/
bedroom    /ˈbedruːm/
beer    /bɪə/
before    /bɪˈfɔː/
begin    /bɪˈɡɪn/
beginning    /bɪˈɡɪnɪŋ/
behave    /bɪˈheɪv/
behaviour    /bɪˈheɪvjə/
behind    /bɪˈhaɪnd/
being    /ˈbiːɪŋ/
belief    /bɪˈliːf/
believe    /bɪˈliːv/
bell    /bel/
belong    /bɪˈlɒŋ/
below    /bɪˈləʊ/
belt    /belt/
bend    /bend/
benefit    /ˈbenɪfɪt/
beside    /bɪˈsaɪd/
best    /best/
bet    /bet/
better    /ˈbetə/
between    /bɪˈtwiːn/
beyond    /bɪˈjɒnd/
bicycle    /ˈbaɪsɪkəl/
big    /bɪɡ/
bill    /bɪl/
bin    /bɪn/
biology    /baɪˈɒlədʒi/
bird    /bɜːd/
birth    /bɜːθ/
birthday    /ˈbɜːθdeɪ/
bit    /bɪt/
bite    /baɪt/
black    /blæk/
blade    /bleɪd/
blame    /bleɪm/
blank    /blæŋk/
block    /blɒk/
blood    /blʌd/
blow    /bləʊ/
blue    /bluː/
board    /bɔːd/
boat    /bəʊt/
body    /ˈbɒdi/
boil    /bɔɪl/
bomb    /bɒm/
bond    /bɒnd/
bone    /bəʊn/
book    /bʊk/
border    /ˈbɔːdə/
bore    /bɔː/
boring    /ˈbɔːrɪŋ/
born    /bɔːn/
borrow    /ˈbɒrəʊ/
boss    /bɒs/
both    /bəʊθ/
bother    /ˈbɒðə/
bottle    /ˈbɒtl/
bottom    /ˈbɒtəm/
boundary    /ˈbaʊndəri/
bow    /baʊ/
bowl    /bəʊl/
box    /bɒks/
boy    /bɔɪ/
brain    /breɪn/
branch    /brɑːntʃ/
brand    /brænd/
brave    /breɪv/
bread    /bred/
break    /breɪk/
breakfast    /ˈbrekfəst/
breathe    /briːð/
brick    /brɪk/
bridge    /brɪdʒ/
brief    /briːf/
bright    /braɪt/
brilliant    /ˈbrɪljənt/
bring    /brɪŋ/
broad    /brɔːd/
broadcast    /ˈbrɔːdkɑːst/
brother    /ˈbrʌðə/
brown    /braʊn/
brush    /brʌʃ/
build    /bɪld/
building    /ˈbɪldɪŋ/
bullet    /ˈbʊlɪt/
bunch    /bʌntʃ/
burn    /bɜːn/
burst    /bɜːst/
bus    /bʌs/
bush    /bʊʃ/
business    /ˈbɪznəs/
busy    /ˈbɪzi/
but    /bʌt/
butter    /ˈbʌtə/
button    /ˈbʌtən/
buy    /baɪ/
by    /baɪ/
cabbage    /ˈkæbɪdʒ/
cabin    /ˈkæbɪn/
cabinet    /ˈkæbɪnət/
cable    /ˈkeɪbəl/
cake    /keɪk/
calculate    /ˈkælkjʊleɪt/
call    /kɔːl/
calm    /kɑːm/
camera    /ˈkæmərə/
camp    /kæmp/
campaign    /kæmˈpeɪn/
campus    /ˈkæmpəs/
can    /kæn/
cancel    /ˈkænsəl/
cancer    /ˈkænsə/
candidate    /ˈkændɪdət/
cap    /kæp/
capable    /ˈkeɪpəbl/
capacity    /kəˈpæsəti/
capital    /ˈkæpɪtəl/
captain    /ˈkæptɪn/
capture    /ˈkæptʃə/
car    /kɑː/
card    /kɑːd/
care    /keə/
career    /kəˈrɪə/
careful    /ˈkeəfəl/
carefully    /ˈkeəfəli/
carry    /ˈkæri/
case    /keɪs/
cash    /kæʃ/
cast    /kɑːst/
cat    /kæt/
catch    /kætʃ/
category    /ˈkætəɡəri/
cause    /kɔːz/
cease    /siːs/
ceiling    /ˈsiːlɪŋ/
celebrate    /ˈseləbreɪt/
cell    /sel/
cent    /sent/
centre    /ˈsentə/
century    /ˈsentʃəri/
ceremony    /ˈserəməni/
certain    /ˈsɜːtən/
certainly    /ˈsɜːtənli/
chain    /tʃeɪn/
chair    /tʃeə/
chairman    /ˈtʃeəmən/
challenge    /ˈtʃælɪndʒ/
chance    /tʃɑːns/
change    /tʃeɪndʒ/
channel    /ˈtʃænəl/
chapter    /ˈtʃæptə/
character    /ˈkærɪktə/
charge    /tʃɑːdʒ/
cheap    /tʃiːp/
check    /tʃek/
cheek    /tʃiːk/
cheerful    /ˈtʃɪəfəl/
cheese    /tʃiːz/
chemical    /ˈkemɪkəl/
chemist    /ˈkemɪst/
cheque    /tʃek/
chest    /tʃest/
chicken    /ˈtʃɪkɪn/
chief    /tʃiːf/
child    /tʃaɪld/
childhood    /ˈtʃaɪldhʊd/
chip    /tʃɪp/
choice    /tʃɔɪs/
choose    /tʃuːz/
church    /tʃɜːtʃ/
cigarette    /ˌsɪɡəˈret/
circle    /ˈsɜːkəl/
circumstance    /ˈsɜːkəmstəns/
citizen    /ˈsɪtɪzən/
city    /ˈsɪti/
civil    /ˈsɪvəl/
claim    /kleɪm/
class    /klɑːs/
classic    /ˈklæsɪk/
classroom    /ˈklɑːsruːm/
clean    /kliːn/
clear    /klɪə/
clearly    /ˈklɪəli/
clerk    /klɑːk/
clever    /ˈklevə/
click    /klɪk/
client    /ˈklaɪənt/
climate    /ˈklaɪmət/
climb    /klaɪm/
clock    /klɒk/
close    /kləʊz/
closed    /kləʊzd/
cloth    /klɒθ/
clothes    /kləʊðz/
cloud    /klaʊd/
club    /klʌb/
coach    /kəʊtʃ/
coal    /kəʊl/
coast    /kəʊst/
coat    /kəʊt/
code    /kəʊd/
coffee    /ˈkɒfi/
coin    /kɔɪn/
cold    /kəʊld/
collapse    /kəˈlæps/
colleague    /ˈkɒliːɡ/
collect    /kəˈlekt/
collection    /kəˈlekʃən/
college    /ˈkɒlɪdʒ/
colour    /ˈkʌlə/
column    /ˈkɒləm/
combination    /ˌkɒmbɪˈneɪʃən/
combine    /kəmˈbaɪn/
come    /kʌm/
comedy    /ˈkɒmədi/
comfort    /ˈkʌmfət/
comfortable    /ˈkʌmfətəbl/
command    /kəˈmɑːnd/
comment    /ˈkɒment/
commercial    /kəˈmɜːʃəl/
commission    /kəˈmɪʃən/
commit    /kəˈmɪt/
commitment    /kəˈmɪtmənt/
committee    /kəˈmɪti/
common    /ˈkɒmən/
communicate    /kəˈmjuːnɪkeɪt/
communication    /kəˌmjuːnɪˈkeɪʃən/
community    /kəˈmjuːnəti/
company    /ˈkʌmpəni/
compare    /kəmˈpeə/
comparison    /kəmˈpærɪsən/
compete    /kəmˈpiːt/
competition    /ˌkɒmpəˈtɪʃən/
complain    /kəmˈpleɪn/
complaint    /kəmˈpleɪnt/
complete    /kəmˈpliːt/
completely    /kəmˈpliːtli/
complex    /ˈkɒmpleks/
complicated    /ˈkɒmplɪkeɪtɪd/
component    /kəmˈpəʊnənt/
computer    /kəmˈpjuːtə/
concentrate    /ˈkɒnsəntreɪt/
concentration    /ˌkɒnsənˈtreɪʃən/
concept    /ˈkɒnsept/
concern    /kənˈsɜːn/
concert    /ˈkɒnsət/
conclude    /kənˈkluːd/
conclusion    /kənˈkluːʒən/
condition    /kənˈdɪʃən/
conduct    /kənˈdʌkt/
conference    /ˈkɒnfərəns/
confidence    /ˈkɒnfɪdəns/
confident    /ˈkɒnfɪdənt/
confirm    /kənˈfɜːm/
conflict    /ˈkɒnflɪkt/
confuse    /kənˈfjuːz/
confusion    /kənˈfjuːʒən/
connect    /kəˈnekt/
connection    /kəˈnekʃən/
consequence    /ˈkɒnsɪkwəns/
conservative    /kənˈsɜːvətɪv/
consider    /kənˈsɪdə/
considerable    /kənˈsɪdərəbl/
consist    /kənˈsɪst/
constant    /ˈkɒnstənt/
constantly    /ˈkɒnstəntli/
construct    /kənˈstrʌkt/
construction    /kənˈstrʌkʃən/
consult    /kənˈsʌlt/
consumer    /kənˈsjuːmə/
contact    /ˈkɒntækt/
contain    /kənˈteɪn/
container    /kənˈteɪnə/
contemporary    /kənˈtempərəri/
content    /ˈkɒntent/
contest    /ˈkɒntest/
context    /ˈkɒntekst/
continent    /ˈkɒntɪnənt/
continue    /kənˈtɪnjuː/
contract    /ˈkɒntrækt/
contrast    /ˈkɒntrɑːst/
contribute    /kənˈtrɪbjuːt/
contribution    /ˌkɒntrɪˈbjuːʃən/
control    /kənˈtrəʊl/
convenient    /kənˈviːniənt/
conversation    /ˌkɒnvəˈseɪʃən/
convert    /kənˈvɜːt/
convince    /kənˈvɪns/
cook    /kʊk/
cooker    /ˈkʊkə/
cookie    /ˈkʊki/
cool    /kuːl/
cooperate    /kəʊˈɒpəreɪt/
copy    /ˈkɒpi/
corner    /ˈkɔːnə/
correct    /kəˈrekt/
cost    /kɒst/
cottage    /ˈkɒtɪdʒ/
cotton    /ˈkɒtən/
cough    /kɒf/
could    /kʊd/
council    /ˈkaʊnsəl/
count    /kaʊnt/
country    /ˈkʌntri/
county    /ˈkaʊnti/
couple    /ˈkʌpl/
courage    /ˈkʌrɪdʒ/
course    /kɔːs/
court    /kɔːt/
cousin    /ˈkʌzən/
cover    /ˈkʌvə/
cow    /kaʊ/
crack    /kræk/
craft    /krɑːft/
crash    /kræʃ/
crazy    /ˈkreɪzi/
cream    /kriːm/
create    /kriˈeɪt/
creation    /kriˈeɪʃən/
creative    /kriˈeɪtɪv/
creature    /ˈkriːtʃə/
credit    /ˈkredɪt/
crew    /kruː/
crime    /kraɪm/
criminal    /ˈkrɪmɪnəl/
crisis    /ˈkraɪsɪs/
criterion    /kraɪˈtɪəriən/
critic    /ˈkrɪtɪk/
critical    /ˈkrɪtɪkəl/
criticism    /ˈkrɪtɪsɪzəm/
criticize    /ˈkrɪtɪsaɪz/
crop    /krɒp/
cross    /krɒs/
crowd    /kraʊd/
crown    /kraʊn/
crucial    /ˈkruːʃəl/
cry    /kraɪ/
cultural    /ˈkʌltʃərəl/
culture    /ˈkʌltʃə/
cup    /kʌp/
cupboard    /ˈkʌbəd/
curious    /ˈkjʊəriəs/
currency    /ˈkʌrənsi/
current    /ˈkʌrənt/
curtain    /ˈkɜːtən/
curve    /kɜːv/
custom    /ˈkʌstəm/
customer    /ˈkʌstəmə/
cut    /kʌt/
cycle    /ˈsaɪkəl/
dad    /dæd/
daily    /ˈdeɪli/
damage    /ˈdæmɪdʒ/
dance    /dɑːns/
danger    /ˈdeɪndʒə/
dangerous    /ˈdeɪndʒərəs/
dare    /deə/
dark    /dɑːk/
data    /ˈdeɪtə/
date    /deɪt/
daughter    /ˈdɔːtə/
day    /deɪ/
dead    /ded/
deal    /diːl/
dear    /dɪə/
death    /deθ/
debate    /dɪˈbeɪt/
debt    /det/
decade    /ˈdekeɪd/
decide    /dɪˈsaɪd/
decision    /dɪˈsɪʒən/
declare    /dɪˈkleə/
decline    /dɪˈklaɪn/
decorate    /ˈdekəreɪt/
decrease    /dɪˈkriːs/
deep    /diːp/
defeat    /dɪˈfiːt/
defend    /dɪˈfend/
define    /dɪˈfaɪn/
definite    /ˈdefɪnɪt/
definitely    /ˈdefɪnətli/
degree    /dɪˈɡriː/
delay    /dɪˈleɪ/
deliver    /dɪˈlɪvə/
delivery    /dɪˈlɪvəri/
demand    /dɪˈmɑːnd/
democracy    /dɪˈmɒkrəsi/
demonstrate    /ˈdemənstreɪt/
deny    /dɪˈnaɪ/
department    /dɪˈpɑːtmənt/
depend    /dɪˈpend/
deposit    /dɪˈpɒzɪt/
depress    /dɪˈpres/
depth    /depθ/
describe    /dɪˈskraɪb/
description    /dɪˈskrɪpʃən/
desert    /ˈdezət/
deserve    /dɪˈzɜːv/
design    /dɪˈzaɪn/
designer    /dɪˈzaɪnə/
desire    /dɪˈzaɪə/
desk    /desk/
desperate    /ˈdespərət/
despite    /dɪˈspaɪt/
destroy    /dɪˈstrɔɪ/
detail    /ˈdiːteɪl/
detect    /dɪˈtekt/
develop    /dɪˈveləp/
development    /dɪˈveləpmənt/
device    /dɪˈvaɪs/
devote    /dɪˈvəʊt/
dialogue    /ˈdaɪəlɒɡ/
diamond    /ˈdaɪəmənd/
diary    /ˈdaɪəri/
die    /daɪ/
diet    /ˈdaɪət/
differ    /ˈdɪfə/
difference    /ˈdɪfərəns/
different    /ˈdɪfərənt/
difficult    /ˈdɪfɪkəlt/
difficulty    /ˈdɪfɪkəlti/
dig    /dɪɡ/
dimension    /daɪˈmenʃən/
dinner    /ˈdɪnə/
direct    /dəˈrekt/
direction    /dəˈrekʃən/
director    /dəˈrektə/
dirt    /dɜːt/
dirty    /ˈdɜːti/
disagree    /ˌdɪsəˈɡriː/
disappear    /ˌdɪsəˈpɪə/
disappoint    /ˌdɪsəˈpɔɪnt/
disaster    /dɪˈzɑːstə/
discipline    /ˈdɪsɪplɪn/
discount    /ˈdɪskaʊnt/
discover    /dɪˈskʌvə/
discovery    /dɪˈskʌvəri/
discuss    /dɪˈskʌs/
discussion    /dɪˈskʌʃən/
disease    /dɪˈziːz/
dish    /dɪʃ/
dismiss    /dɪsˈmɪs/
display    /dɪˈspleɪ/
distance    /ˈdɪstəns/
distinct    /dɪˈstɪŋkt/
distinguish    /dɪˈstɪŋɡwɪʃ/
distribute    /dɪˈstrɪbjuːt/
district    /ˈdɪstrɪkt/
divide    /dɪˈvaɪd/
division    /dɪˈvɪʒən/
divorce    /dɪˈvɔːs/
do    /duː/
doctor    /ˈdɒktə/
document    /ˈdɒkjʊmənt/
dog    /dɒɡ/
door    /dɔː/
double    /ˈdʌbəl/
doubt    /daʊt/
down    /daʊn/
download    /ˌdaʊnˈləʊd/
downstairs    /ˌdaʊnˈsteəz/
dozen    /ˈdʌzən/
draft    /drɑːft/
drag    /dræɡ/
drama    /ˈdrɑːmə/
draw    /drɔː/
drawer    /drɔːə/
drawing    /ˈdrɔːɪŋ/
dream    /driːm/
dress    /dres/
drink    /drɪŋk/
drive    /draɪv/
driver    /ˈdraɪvə/
drop    /drɒp/
drug    /drʌɡ/
dry    /draɪ/
due    /djuː/
during    /ˈdjʊərɪŋ/
dust    /dʌst/
duty    /ˈdjuːti/
each    /iːtʃ/
ear    /ɪə/
early    /ˈɜːli/
earn    /ɜːn/
earth    /ɜːθ/
ease    /iːz/
easily    /ˈiːzɪli/
east    /iːst/
easy    /ˈiːzi/
eat    /iːt/
economic    /ˌiːkəˈnɒmɪk/
economy    /ɪˈkɒnəmi/
edge    /edʒ/
edition    /ɪˈdɪʃən/
editor    /ˈedɪtə/
education    /ˌedʒʊˈkeɪʃən/
effect    /ɪˈfekt/
effective    /ɪˈfektɪv/
efficient    /ɪˈfɪʃənt/
effort    /ˈefət/
egg    /eɡ/
eight    /eɪt/
either    /ˈaɪðə/
elbow    /ˈelbəʊ/
elderly    /ˈeldəli/
elect    /ɪˈlekt/
election    /ɪˈlekʃən/
electric    /ɪˈlektrɪk/
electricity    /ɪˌlekˈtrɪsɪti/
electronic    /ɪˌlekˈtrɒnɪk/
element    /ˈelɪmənt/
else    /els/
email    /ˈiːmeɪl/
embarrass    /ɪmˈbærəs/
emerge    /ɪˈmɜːdʒ/
emotion    /ɪˈməʊʃən/
emotional    /ɪˈməʊʃənəl/
emphasis    /ˈemfəsɪs/
employ    /ɪmˈplɔɪ/
employee    /ˌemplɔɪˈiː/
employer    /ɪmˈplɔɪə/
employment    /ɪmˈplɔɪmənt/
empty    /ˈempti/
end    /end/
enemy    /ˈenəmi/
energy    /ˈenədʒi/
engine    /ˈendʒɪn/
engineer    /ˌendʒɪˈnɪə/
enjoy    /ɪnˈdʒɔɪ/
enormous    /ɪˈnɔːməs/
enough    /ɪˈnʌf/
ensure    /ɪnˈʃɔː/
enter    /ˈentə/
entertain    /ˌentəˈteɪn/
entertainment    /ˌentəˈteɪnmənt/
enthusiasm    /ɪnˈθjuːziæzəm/
entire    /ɪnˈtaɪə/
entirely    /ɪnˈtaɪəli/
entrance    /ˈentrəns/
entry    /ˈentri/
environment    /ɪnˈvaɪrənmənt/
equal    /ˈiːkwəl/
equipment    /ɪˈkwɪpmənt/
error    /ˈerə/
escape    /ɪˈskeɪp/
especially    /ɪˈspeʃəli/
essay    /ˈeseɪ/
essential    /ɪˈsenʃəl/
establish    /ɪˈstæblɪʃ/
estate    /ɪˈsteɪt/
estimate    /ˈestɪmeɪt/
even    /ˈiːvən/
evening    /ˈiːvnɪŋ/
event    /ɪˈvent/
eventually    /ɪˈventʃuəli/
ever    /ˈevə/
every    /ˈevri/
everybody    /ˈevribɒdi/
everyday    /ˈevrideɪ/
everyone    /ˈevriwʌn/
everything    /ˈevriθɪŋ/
everywhere    /ˈevriweə/
evidence    /ˈevɪdəns/
evil    /ˈiːvəl/
exact    /ɪɡˈzækt/
exactly    /ɪɡˈzæktli/
examination    /ɪɡˌzæmɪˈneɪʃən/
example    /ɪɡˈzɑːmpl/
excellent    /ˈeksələnt/
except    /ɪkˈsept/
exchange    /ɪksˈtʃeɪndʒ/
excite    /ɪkˈsaɪt/
excitement    /ɪkˈsaɪtmənt/
exciting    /ɪkˈsaɪtɪŋ/
excuse    /ɪkˈskjuːz/
exercise    /ˈeksəsaɪz/
exist    /ɪɡˈzɪst/
existence    /ɪɡˈzɪstəns/
expect    /ɪkˈspekt/
expectation    /ˌekspekˈteɪʃən/
expense    /ɪkˈspens/
expensive    /ɪkˈspensɪv/
experience    /ɪkˈspɪəriəns/
experiment    /ɪkˈsperɪmənt/
expert    /ˈekspɜːt/
explain    /ɪkˈspleɪn/
explanation    /ˌekspləˈneɪʃən/
explode    /ɪkˈspləʊd/
explore    /ɪkˈsplɔː/
explosion    /ɪkˈspləʊʒən/
export    /ˈekspɔːt/
express    /ɪkˈspres/
expression    /ɪkˈspreʃən/
extend    /ɪkˈstend/
extent    /ɪkˈstent/
extra    /ˈekstrə/
eye    /aɪ/
face    /feɪs/
facility    /fəˈsɪləti/
fact    /fækt/
factor    /ˈfæktə/
factory    /ˈfæktri/
fail    /feɪl/
failure    /ˈfeɪljə/
fair    /feə/
fairly    /ˈfeəli/
faith    /feɪθ/
fall    /fɔːl/
false    /fɔːls/
familiar    /fəˈmɪliə/
family    /ˈfæmɪli/
famous    /ˈfeɪməs/
fan    /fæn/
fancy    /ˈfænsi/
far    /fɑː/
farm    /fɑːm/
farmer    /ˈfɑːmə/
fashion    /ˈfæʃən/
fast    /fɑːst/
fat    /fæt/
father    /ˈfɑːðə/
fault    /fɔːlt/
favour    /ˈfeɪvə/
favourite    /ˈfeɪvərɪt/
fear    /fɪə/
feature    /ˈfiːtʃə/
fee    /fiː/
feed    /fiːd/
feel    /fiːl/
feeling    /ˈfiːlɪŋ/
fellow    /ˈfeləʊ/
female    /ˈfiːmeɪl/
fence    /fens/
festival    /ˈfestɪvəl/
fetch    /fetʃ/
few    /fjuː/
field    /fiːld/
fight    /faɪt/
figure    /ˈfɪɡə/
file    /faɪl/
fill    /fɪl/
film    /fɪlm/
final    /ˈfaɪnəl/
finally    /ˈfaɪnəli/
finance    /ˈfaɪnæns/
financial    /faɪˈnænʃəl/
find    /faɪnd/
fine    /faɪn/
finger    /ˈfɪŋɡə/
finish    /ˈfɪnɪʃ/
fire    /ˈfaɪə/
firm    /fɜːm/
first    /fɜːst/
fish    /fɪʃ/
fit    /fɪt/
five    /faɪv/
fix    /fɪks/
flag    /flæɡ/
flat    /flæt/
flavour    /ˈfleɪvə/
flesh    /fleʃ/
flight    /flaɪt/
float    /fləʊt/
floor    /flɔː/
flow    /fləʊ/
flower    /ˈflaʊə/
fly    /flaɪ/
focus    /ˈfəʊkəs/
fold    /fəʊld/
folk    /fəʊk/
follow    /ˈfɒləʊ/
food    /fuːd/
fool    /fuːl/
foot    /fʊt/
football    /ˈfʊtbɔːl/
for    /fə/
force    /fɔːs/
foreign    /ˈfɒrɪn/
forest    /ˈfɒrɪst/
forget    /fəˈɡet/
forgive    /fəˈɡɪv/
form    /fɔːm/
formal    /ˈfɔːməl/
former    /ˈfɔːmə/
fortunately    /ˈfɔːtʃənətli/
fortune    /ˈfɔːtʃuːn/
forward    /ˈfɔːwəd/
found    /faʊnd/
foundation    /faʊnˈdeɪʃən/
frame    /freɪm/
free    /friː/
freedom    /ˈfriːdəm/
freeze    /friːz/
frequent    /ˈfriːkwənt/
fresh    /freʃ/
friend    /frend/
friendly    /ˈfrendli/
friendship    /ˈfrendʃɪp/
from    /frəm/
front    /frʌnt/
fruit    /fruːt/
fuel    /fjʊəl/
full    /fʊl/
fun    /fʌn/
function    /ˈfʌŋkʃən/
fund    /fʌnd/
fundamental    /ˌfʌndəˈmentəl/
funeral    /ˈfjuːnərəl/
funny    /ˈfʌni/
furniture    /ˈfɜːnɪtʃə/
further    /ˈfɜːðə/
future    /ˈfjuːtʃə/
gain    /ɡeɪn/
gallery    /ˈɡæləri/
game    /ɡeɪm/
gap    /ɡæp/
garage    /ˈɡærɑːʒ/
garden    /ˈɡɑːdn/
gas    /ɡæs/
gate    /ɡeɪt/
gather    /ˈɡæðə/
general    /ˈdʒenrəl/
generally    /ˈdʒenrəli/
generate    /ˈdʒenəreɪt/
generation    /ˌdʒenəˈreɪʃən/
generous    /ˈdʒenərəs/
gentle    /ˈdʒentl/
gentleman    /ˈdʒentlmən/
geography    /dʒiˈɒɡrəfi/
get    /ɡet/
gift    /ɡɪft/
girl    /ɡɜːl/
girlfriend    /ˈɡɜːlfrend/
give    /ɡɪv/
glad    /ɡlæd/
glass    /ɡlɑːs/
global    /ˈɡləʊbəl/
glove    /ɡlʌv/
go    /ɡəʊ/
goal    /ɡəʊl/
god    /ɡɒd/
gold    /ɡəʊld/
golf    /ɡɒlf/
good    /ɡʊd/
goodbye    /ˌɡʊdˈbaɪ/
goods    /ɡʊdz/
government    /ˈɡʌvənmənt/
grab    /ɡræb/
grade    /ɡreɪd/
gradually    /ˈɡrædʒuəli/
grain    /ɡreɪn/
grammar    /ˈɡræmə/
grand    /ɡrænd/
grandfather    /ˈɡrænfɑːðə/
grandmother    /ˈɡrænmʌðə/
grant    /ɡrɑːnt/
grass    /ɡrɑːs/
grateful    /ˈɡreɪtfəl/
great    /ɡreɪt/
green    /ɡriːn/
grey    /ɡreɪ/
ground    /ɡraʊnd/
group    /ɡruːp/
grow    /ɡrəʊ/
growth    /ɡrəʊθ/
guarantee    /ˌɡærənˈtiː/
guard    /ɡɑːd/
guess    /ɡes/
guest    /ɡest/
guide    /ɡaɪd/
guilty    /ˈɡɪlti/
gun    /ɡʌn/
guy    /ɡaɪ/
habit    /ˈhæbɪt/
hair    /heə/
half    /hɑːf/
hall    /hɔːl/
hammer    /ˈhæmə/
hand    /hænd/
handle    /ˈhændəl/
handsome    /ˈhænsəm/
hang    /hæŋ/
happen    /ˈhæpən/
happy    /ˈhæpi/
hard    /hɑːd/
hardly    /ˈhɑːdli/
harm    /hɑːm/
hat    /hæt/
hate    /heɪt/
have    /hæv/
he    /hiː/
head    /hed/
health    /helθ/
healthy    /ˈhelθi/
hear    /hɪə/
heart    /hɑːt/
heat    /hiːt/
heaven    /ˈhevən/
heavy    /ˈhevi/
heel    /hiːl/
height    /haɪt/
helicopter    /ˈhelɪkɒptə/
hell    /hel/
hello    /həˈləʊ/
help    /help/
helpful    /ˈhelpfəl/
hence    /hens/
her    /hɜː/
here    /hɪə/
hero    /ˈhɪərəʊ/
herself    /həˈself/
hey    /heɪ/
hide    /haɪd/
high    /haɪ/
highly    /ˈhaɪli/
hill    /hɪl/
him    /hɪm/
himself    /hɪmˈself/
hire    /ˈhaɪə/
his    /hɪz/
history    /ˈhɪstəri/
hit    /hɪt/
hold    /həʊld/
hole    /həʊl/
holiday    /ˈhɒlədeɪ/
holy    /ˈhəʊli/
home    /həʊm/
honest    /ˈɒnɪst/
honey    /ˈhʌni/
honour    /ˈɒnə/
hope    /həʊp/
horse    /hɔːs/
hospital    /ˈhɒspɪtəl/
host    /həʊst/
hot    /hɒt/
hotel    /həʊˈtel/
hour    /ˈaʊə/
house    /haʊs/
household    /ˈhaʊshəʊld/
housing    /ˈhaʊzɪŋ/
how    /haʊ/
however    /haʊˈevə/
huge    /hjuːdʒ/
human    /ˈhjuːmən/
humour    /ˈhjuːmə/
hundred    /ˈhʌndrəd/
hungry    /ˈhʌŋɡri/
hunt    /hʌnt/
hurry    /ˈhʌri/
hurt    /hɜːt/
husband    /ˈhʌzbənd/
hypothesis    /haɪˈpɒθəsɪs/
ice    /aɪs/
idea    /aɪˈdɪə/
ideal    /aɪˈdɪəl/
identify    /aɪˈdentɪfaɪ/
identity    /aɪˈdentɪti/
ignore    /ɪɡˈnɔː/
ill    /ɪl/
illegal    /ɪˈliːɡəl/
illness    /ˈɪlnəs/
illustrate    /ˈɪləstreɪt/
image    /ˈɪmɪdʒ/
imagination    /ɪˌmædʒɪˈneɪʃən/
imagine    /ɪˈmædʒɪn/
immediate    /ɪˈmiːdiət/
immediately    /ɪˈmiːdiətli/
impact    /ˈɪmpækt/
imply    /ɪmˈplaɪ/
import    /ˈɪmpɔːt/
importance    /ɪmˈpɔːtəns/
important    /ɪmˈpɔːtənt/
impose    /ɪmˈpəʊz/
impossible    /ɪmˈpɒsəbl/
impress    /ɪmˈpres/
impression    /ɪmˈpreʃən/
improve    /ɪmˈpruːv/
improvement    /ɪmˈpruːvmənt/
incident    /ˈɪnsɪdənt/
include    /ɪnˈkluːd/
including    /ɪnˈkluːdɪŋ/
income    /ˈɪnkʌm/
increase    /ɪnˈkriːs/
increasingly    /ɪnˈkriːsɪŋli/
indeed    /ɪnˈdiːd/
independent    /ˌɪndɪˈpendənt/
index    /ˈɪndeks/
indicate    /ˈɪndɪkeɪt/
individual    /ˌɪndɪˈvɪdʒuəl/
industry    /ˈɪndəstri/
inevitable    /ɪnˈevɪtəbl/
infect    /ɪnˈfekt/
influence    /ˈɪnfluəns/
inform    /ɪnˈfɔːm/
information    /ˌɪnfəˈmeɪʃən/
ingredient    /ɪnˈɡriːdiənt/
initial    /ɪˈnɪʃəl/
initiative    /ɪˈnɪʃətɪv/
injury    /ˈɪndʒəri/
inner    /ˈɪnə/
innocent    /ˈɪnəsənt/
inquiry    /ɪnˈkwaɪəri/
inside    /ɪnˈsaɪd/
insist    /ɪnˈsɪst/
inspire    /ɪnˈspaɪə/
install    /ɪnˈstɔːl/
instance    /ˈɪnstəns/
instead    /ɪnˈsted/
institution    /ˌɪnstɪˈtjuːʃən/
instruction    /ɪnˈstrʌkʃən/
instrument    /ˈɪnstrəmənt/
insurance    /ɪnˈʃʊərəns/
intelligence    /ɪnˈtelɪdʒəns/
intelligent    /ɪnˈtelɪdʒənt/
intend    /ɪnˈtend/
intention    /ɪnˈtenʃən/
interest    /ˈɪntrəst/
interior    /ɪnˈtɪəriə/
internal    /ɪnˈtɜːnəl/
international    /ˌɪntəˈnæʃənəl/
internet    /ˈɪntənet/
interpret    /ɪnˈtɜːprɪt/
interrupt    /ˌɪntəˈrʌpt/
interval    /ˈɪntəvəl/
interview    /ˈɪntəvjuː/
into    /ˈɪntuː/
introduce    /ˌɪntrəˈdjuːs/
introduction    /ˌɪntrəˈdʌkʃən/
invent    /ɪnˈvent/
invention    /ɪnˈvenʃən/
invest    /ɪnˈvest/
investigate    /ɪnˈvestɪɡeɪt/
investment    /ɪnˈvestmənt/
invite    /ɪnˈvaɪt/
involve    /ɪnˈvɒlv/
iron    /ˈaɪən/
island    /ˈaɪlənd/
issue    /ˈɪʃuː/
it    /ɪt/
item    /ˈaɪtəm/
its    /ɪts/
itself    /ɪtˈself/
jacket    /ˈdʒækɪt/
jam    /dʒæm/
job    /dʒɒb/
join    /dʒɔɪn/
joint    /dʒɔɪnt/
joke    /dʒəʊk/
journal    /ˈdʒɜːnəl/
journalist    /ˈdʒɜːnəlɪst/
journey    /ˈdʒɜːni/
joy    /dʒɔɪ/
judge    /dʒʌdʒ/
juice    /dʒuːs/
jump    /dʒʌmp/
junior    /ˈdʒuːniə/
jury    /ˈdʒʊəri/
just    /dʒʌst/
justice    /ˈdʒʌstɪs/
justify    /ˈdʒʌstɪfaɪ/
keep    /kiːp/
key    /kiː/
kick    /kɪk/
kid    /kɪd/
kill    /kɪl/
kind    /kaɪnd/
king    /kɪŋ/
kiss    /kɪs/
kitchen    /ˈkɪtʃɪn/
knee    /niː/
knife    /naɪf/
knock    /nɒk/
know    /nəʊ/
knowledge    /ˈnɒlɪdʒ/
lab    /læb/
label    /ˈleɪbəl/
laboratory    /ləˈbɒrətəri/
labour    /ˈleɪbə/
lack    /læk/
lady    /ˈleɪdi/
lake    /leɪk/
lamp    /læmp/
land    /lænd/
landscape    /ˈlændskeɪp/
language    /ˈlæŋɡwɪdʒ/
large    /lɑːdʒ/
largely    /ˈlɑːdʒli/
last    /lɑːst/
late    /leɪt/
lately    /ˈleɪtli/
later    /ˈleɪtə/
latest    /ˈleɪtɪst/
laugh    /lɑːf/
launch    /lɔːntʃ/
law    /lɔː/
lawyer    /ˈlɔːjə/
lay    /leɪ/
layer    /ˈleɪə/
lazy    /ˈleɪzi/
lead    /liːd/
leader    /ˈliːdə/
leadership    /ˈliːdəʃɪp/
leading    /ˈliːdɪŋ/
leaf    /liːf/
league    /liːɡ/
lean    /liːn/
learn    /lɜːn/
least    /liːst/
leather    /ˈleðə/
leave    /liːv/
lecture    /ˈlektʃə/
left    /left/
leg    /leɡ/
legal    /ˈliːɡəl/
legend    /ˈledʒənd/
leisure    /ˈleʒə/
lend    /lend/
length    /leŋθ/
less    /les/
lesson    /ˈlesən/
let    /let/
letter    /ˈletə/
level    /ˈlevəl/
library    /ˈlaɪbrəri/
license    /ˈlaɪsəns/
lie    /laɪ/
life    /laɪf/
lift    /lɪft/
light    /laɪt/
like    /laɪk/
likely    /ˈlaɪkli/
limit    /ˈlɪmɪt/
line    /laɪn/
link    /lɪŋk/
lip    /lɪp/
liquid    /ˈlɪkwɪd/
list    /lɪst/
listen    /ˈlɪsən/
literature    /ˈlɪtərətʃə/
little    /ˈlɪtl/
live    /lɪv/
load    /ləʊd/
loan    /ləʊn/
local    /ˈləʊkəl/
locate    /ləʊˈkeɪt/
location    /ləʊˈkeɪʃən/
lock    /lɒk/
logical    /ˈlɒdʒɪkəl/
lonely    /ˈləʊnli/
long    /lɒŋ/
look    /lʊk/
loose    /luːs/
lord    /lɔːd/
lorry    /ˈlɒri/
lose    /luːz/
loss    /lɒs/
lot    /lɒt/
loud    /laʊd/
love    /lʌv/
lovely    /ˈlʌvli/
low    /ləʊ/
lower    /ˈləʊə/
luck    /lʌk/
lucky    /ˈlʌki/
lunch    /lʌntʃ/
lung    /lʌŋ/
machine    /məˈʃiːn/
mad    /mæd/
magazine    /ˌmæɡəˈziːn/
magic    /ˈmædʒɪk/
mail    /meɪl/
main    /meɪn/
mainly    /ˈmeɪnli/
maintain    /meɪnˈteɪn/
major    /ˈmeɪdʒə/
majority    /məˈdʒɒrɪti/
make    /meɪk/
male    /meɪl/
mall    /mɔːl/
man    /mæn/
manage    /ˈmænɪdʒ/
management    /ˈmænɪdʒmənt/
manager    /ˈmænɪdʒə/
manner    /ˈmænə/
manufacture    /ˌmænjuˈfæktʃə/
many    /ˈmeni/
map    /mæp/
market    /ˈmɑːkɪt/
marriage    /ˈmærɪdʒ/
married    /ˈmærid/
marry    /ˈmæri/
mass    /mæs/
master    /ˈmɑːstə/
match    /mætʃ/
material    /məˈtɪəriəl/
matter    /ˈmætə/
may    /meɪ/
maybe    /ˈmeɪbi/
meal    /mɪəl/
mean    /miːn/
meaning    /ˈmiːnɪŋ/
means    /miːnz/
measure    /ˈmeʒə/
meat    /miːt/
mechanic    /məˈkænɪk/
media    /ˈmiːdiə/
medical    /ˈmedɪkəl/
medicine    /ˈmedɪsɪn/
medium    /ˈmiːdiəm/
meet    /miːt/
meeting    /ˈmiːtɪŋ/
member    /ˈmembə/
memory    /ˈmeməri/
mention    /ˈmenʃən/
menu    /ˈmenjuː/
mere    /mɪə/
merely    /ˈmɪəli/
message    /ˈmesɪdʒ/
metal    /ˈmetl/
method    /ˈmeθəd/
middle    /ˈmɪdl/
might    /maɪt/
mile    /maɪl/
military    /ˈmɪlɪtəri/
milk    /mɪlk/
mill    /mɪl/
mind    /maɪnd/
mine    /maɪn/
minister    /ˈmɪnɪstə/
ministry    /ˈmɪnɪstri/
minute    /ˈmɪnɪt/
mirror    /ˈmɪrə/
miss    /mɪs/
mistake    /mɪˈsteɪk/
mix    /mɪks/
mixture    /ˈmɪkstʃə/
mobile    /ˈməʊbaɪl/
mode    /məʊd/
model    /ˈmɒdl/
modern    /ˈmɒdən/
moment    /ˈməʊmənt/
money    /ˈmʌni/
month    /mʌnθ/
mood    /muːd/
moon    /muːn/
moral    /ˈmɒrəl/
more    /mɔː/
morning    /ˈmɔːnɪŋ/
most    /məʊst/
mother    /ˈmʌðə/
motion    /ˈməʊʃən/
motor    /ˈməʊtə/
mountain    /ˈmaʊntɪn/
mouth    /maʊθ/
move    /muːv/
movement    /ˈmuːvmənt/
movie    /ˈmuːvi/
much    /mʌtʃ/
mud    /mʌd/
multiple    /ˈmʌltɪpl/
murder    /ˈmɜːdə/
muscle    /ˈmʌsəl/
museum    /mjuːˈziːəm/
music    /ˈmjuːzɪk/
musical    /ˈmjuːzɪkəl/
must    /mʌst/
my    /maɪ/
myself    /maɪˈself/
mystery    /ˈmɪstəri/
nail    /neɪl/
name    /neɪm/
narrow    /ˈnærəʊ/
nation    /ˈneɪʃən/
national    /ˈnæʃənəl/
native    /ˈneɪtɪv/
natural    /ˈnætʃərəl/
nature    /ˈneɪtʃə/
near    /nɪə/
nearly    /ˈnɪəli/
neat    /niːt/
necessary    /ˈnesəsəri/
neck    /nek/
need    /niːd/
negative    /ˈneɡətɪv/
neighbour    /ˈneɪbə/
neither    /ˈnaɪðə/
nerve    /nɜːv/
nervous    /ˈnɜːvəs/
net    /net/
network    /ˈnetwɜːk/
never    /ˈnevə/
nevertheless    /ˌnevəðəˈles/
new    /njuː/
news    /njuːz/
newspaper    /ˈnjuːzˌpeɪpə/
next    /nekst/
nice    /naɪs/
night    /naɪt/
no    /nəʊ/
noise    /nɔɪz/
none    /nʌn/
nor    /nɔː/
normal    /ˈnɔːməl/
normally    /ˈnɔːməli/
north    /nɔːθ/
northern    /ˈnɔːðən/
nose    /nəʊz/
not    /nɒt/
note    /nəʊt/
nothing    /ˈnʌθɪŋ/
notice    /ˈnəʊtɪs/
novel    /ˈnɒvəl/
now    /naʊ/
nuclear    /ˈnjuːkliə/
number    /ˈnʌmbə/
nurse    /nɜːs/
object    /ˈɒbdʒɪkt/
objective    /əbˈdʒektɪv/
obligation    /ˌɒblɪˈɡeɪʃən/
observation    /ˌɒbzəˈveɪʃən/
observe    /əbˈzɜːv/
obtain    /əbˈteɪn/
obvious    /ˈɒbvɪəs/
obviously    /ˈɒbvɪəsli/
occasion    /əˈkeɪʒən/
occasionally    /əˈkeɪʒənəli/
occupation    /ˌɒkjʊˈpeɪʃən/
occur    /əˈkɜː/
ocean    /ˈəʊʃən/
odd    /ɒd/
of    /ɒv/
off    /ɒf/
offer    /ˈɒfə/
office    /ˈɒfɪs/
officer    /ˈɒfɪsə/
official    /əˈfɪʃəl/
often    /ˈɒfən/
oil    /ɔɪl/
ok    /ˌəʊˈkeɪ/
old    /əʊld/
on    /ɒn/
once    /wʌns/
one    /wʌn/
only    /ˈəʊnli/
onto    /ˈɒntuː/
open    /ˈəʊpən/
operate    /ˈɒpəreɪt/
operation    /ˌɒpəˈreɪʃən/
opinion    /əˈpɪnjən/
opportunity    /ˌɒpəˈtjuːnɪti/
oppose    /əˈpəʊz/
opposite    /ˈɒpəzɪt/
option    /ˈɒpʃən/
or    /ɔː/
orange    /ˈɒrɪndʒ/
order    /ˈɔːdə/
ordinary    /ˈɔːdənəri/
organ    /ˈɔːɡən/
organization    /ˌɔːɡənaɪˈzeɪʃən/
organize    /ˈɔːɡənaɪz/
origin    /ˈɒrɪdʒɪn/
original    /əˈrɪdʒɪnəl/
other    /ˈʌðə/
otherwise    /ˈʌðəwaɪz/
ought    /ɔːt/
our    /ˈaʊə/
ourselves    /aʊəˈselvz/
out    /aʊt/
outcome    /ˈaʊtkʌm/
outside    /ˌaʊtˈsaɪd/
oven    /ˈʌvən/
over    /ˈəʊvə/
overall    /ˈəʊvərɔːl/
owe    /əʊ/
own    /əʊn/
owner    /ˈəʊnə/
pace    /peɪs/
pack    /pæk/
package    /ˈpækɪdʒ/
page    /peɪdʒ/
pain    /peɪn/
painful    /ˈpeɪnfəl/
paint    /peɪnt/
painter    /ˈpeɪntə/
painting    /ˈpeɪntɪŋ/
pair    /peə/
palace    /ˈpælɪs/
pale    /peɪl/

"""

# Hàm xử lý RAW_PHIEN_AM_DATA thành dictionary (map)
def parse_pronunciation_data(raw_data):
    pron_map = {}
    lines = raw_data.strip().split('\n')
    for line in lines:
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            word = parts[0].strip()
            # Loại bỏ dấu / ở đầu và cuối phiên âm
            pron = parts[1].strip().strip('/') 
            pron_map[word] = pron
    return pron_map

pron_map = parse_pronunciation_data(RAW_PHIEN_AM_DATA)

data = [
    ("abandon", "verb", "abandoned", "abandoned", "abandoning", None, "bỏ rơi, từ bỏ", "He decided to abandon his car.", "forsake, desert", "keep, continue"),
    ("ability", "noun", None, None, None, None, "khả năng", "She has the ability to learn quickly.", "capability, skill", "inability, incapacity"),
    ("able", "adj", None, None, None, None, "có thể, có khả năng", "He is able to swim.", "capable, competent", "unable, incapable"),
    ("abortion", "noun", None, None, None, None, "sự phá thai", "Abortion is a controversial topic.", "termination, miscarriage", "continuation, birth"),
    ("about", "adv", None, None, None, None, "khoảng, về", "I was about to leave.", "regarding, concerning", "unrelated, distant"),
    ("above", "adv", None, None, None, None, "ở trên", "The lamp is above the table.", "over, higher", "below, beneath"),
    ("abroad", "adv", None, None, None, None, "ở nước ngoài", "She studied abroad last year.", "overseas, internationally", "domestically, locally"),
    ("absence", "noun", None, None, None, None, "sự vắng mặt", "His absence was noticed.", "nonattendance, lack", "presence, attendance"),
    ("absolute", "adj", None, None, None, None, "tuyệt đối", "She demanded absolute silence.", "complete, total", "partial, limited"),
    ("absolutely", "adv", None, None, None, None, "hoàn toàn", "I absolutely agree.", "totally, completely", "partially, incompletely"),
    ("absorb", "verb", "absorbed", "absorbed", "absorbing", None, "hấp thụ, thu hút", "Plants absorb water from the soil.", "soak up, take in", "reject, expel"),
    ("abuse", "noun", None, None, None, None, "lạm dụng, ngược đãi", "Child abuse is a serious problem.", "mistreatment, exploitation", "care, protection"),
    ("academic", "adj", None, None, None, None, "học thuật", "She has an academic background.", "scholarly, educational", "practical, vocational"),
    ("accept", "verb", "accepted", "accepted", "accepting", None, "chấp nhận", "He accepted the job offer.", "receive, embrace", "reject, decline"),
    ("access", "noun", None, None, None, None, "sự truy cập, lối vào", "Access to the building is restricted.", "entry, admission", "exit, removal"),
    ("accident", "noun", None, None, None, None, "tai nạn", "He was injured in a car accident.", "collision, mishap", "safety, security"),
    ("accompany", "verb", "accompanied", "accompanied", "accompanying", None, "đi cùng, đồng hành", "She accompanied him to the party.", "escort, join", "leave, abandon"),
    ("accomplish", "verb", "accomplished", "accomplished", "accomplishing", None, "hoàn thành, đạt được", "They accomplished their goals.", "achieve, attain", "fail, abandon"),
    ("according", "adv", None, None, None, None, "theo như, tùy theo", "According to the report, sales increased.", "reportedly, supposedly", "disregarding, ignoring"),
    ("account", "noun", None, None, None, None, "tài khoản, bản báo cáo", "He opened a bank account.", "profile, record", "disregard, neglect"),
    ("accurate", "adj", None, None, None, None, "chính xác", "Her report is accurate.", "exact, precise", "inaccurate, wrong"),
    ("accuse", "verb", "accused", "accused", "accusing", None, "buộc tội", "He was accused of theft.", "charge, blame", "defend, excuse"),
    ("achieve", "verb", "achieved", "achieved", "achieving", None, "đạt được", "She achieved her goals.", "accomplish, attain", "fail, abandon"),
    ("achievement", "noun", None, None, None, None, "thành tựu", "Winning the award was a great achievement.", "accomplishment, success", "failure, setback"),
    ("acid", "noun", None, None, None, None, "axit", "Lemon juice contains acid.", "sour, tart", "alkaline, base"),
    ("acknowledge", "verb", "acknowledged", "acknowledged", "acknowledging", None, "công nhận, thừa nhận", "He acknowledged his mistake.", "admit, accept", "deny, reject"),
    ("acquire", "verb", "acquired", "acquired", "acquiring", None, "đạt được, giành được", "She acquired new skills.", "obtain, gain", "lose, forfeit"),
    ("across", "adv", None, None, None, None, "băng qua, ngang qua", "He walked across the street.", "through, over", "along, around"),
    ("act", "verb", "acted", "acted", "acting", None, "hành động, đóng vai", "She acted in a movie.", "perform, play", "refrain, abstain"),
    ("action", "noun", None, None, None, None, "hành động", "We need to take action now.", "deed, act", "inaction, delay"),
    ("active", "adj", None, None, None, None, "năng động, hoạt động", "She is very active in sports.", "energetic, lively", "inactive, passive"),
    ("activist", "noun", None, None, None, None, "nhà hoạt động", "He is an environmental activist.", "campaigner, advocate", "opponent, adversary"),
    ("activity", "noun", None, None, None, None, "hoạt động", "Swimming is a fun activity.", "exercise, action", "inactivity, idleness"),
    ("actor", "noun", None, None, None, None, "diễn viên nam", "He is a famous actor.", "performer, thespian", "non-actor, bystander"),
    ("actress", "noun", None, None, None, None, "diễn viên nữ", "She is a talented actress.", "performer, thespian", "non-actress, bystander"),
    ("actual", "adj", None, None, None, None, "thực tế, thực sự", "The actual cost was higher than expected.", "real, genuine", "theoretical, hypothetical"),
    ("actually", "adv", None, None, None, None, "thực ra, thực sự", "Actually, I don't like coffee.", "in fact, really", "theoretically, supposedly"),
    ("ad", "noun", None, None, None, None, "quảng cáo", "I saw an ad for a new phone.", "advertisement, promo", "ignore, overlook"),
    ("adapt", "verb", "adapted", "adapted", "adapting", None, "thích nghi, điều chỉnh", "She adapted quickly to the new environment.", "adjust, modify", "resist, reject"),
    ("add", "verb", "added", "added", "adding", None, "thêm vào", "Please add some sugar to my tea.", "include, insert", "subtract, remove"),
    ("addition", "noun", None, None, None, None, "sự thêm vào, phép cộng", "The addition of salt improved the taste.", "increase, supplement", "subtraction, reduction"),
    ("additional", "adj", None, None, None, None, "bổ sung, thêm vào", "We need additional information.", "extra, supplementary", "insufficient, inadequate"),
    ("address", "noun", None, None, None, None, "địa chỉ", "What is your home address?", "location, residence", "ignore, overlook"),
    ("adequate", "adj", None, None, None, None, "đầy đủ, thích hợp", "The food was adequate for everyone.", "sufficient, enough", "insufficient, inadequate"),
    ("adjust", "verb", "adjusted", "adjusted", "adjusting", None, "điều chỉnh", "He adjusted the mirror.", "modify, change", "fix, repair"),
    ("adjustment", "noun", None, None, None, None, "sự điều chỉnh", "A small adjustment is needed.", "modification, change", "fix, repair"),
    ("administration", "noun", None, None, None, None, "quản trị, ban quản lý", "The school administration made new rules.", "management, governance", "anarchy, chaos"),
    ("administrator", "noun", None, None, None, None, "người quản trị", "She is the system administrator.", "manager, supervisor", "employee, worker"),
    ("admire", "verb", "admired", "admired", "admiring", None, "ngưỡng mộ", "I admire her courage.", "respect, appreciate", "despise, criticize"),
    ("admission", "noun", None, None, None, None, "sự nhận vào, sự thú nhận", "Admission to the museum is free.", "entry, access", "rejection, denial"),
    ("admit", "verb", "admitted", "admitted", "admitting", None, "thừa nhận, nhận vào", "He admitted his mistake.", "confess, acknowledge", "deny, reject"),
    ("adolescent", "noun", None, None, None, None, "thanh thiếu niên", "The adolescent is going through changes.", "teenager, youth", "adult, elder"),
    ("adopt", "verb", "adopted", "adopted", "adopting", None, "nhận nuôi, áp dụng", "They adopted a child.", "embrace, accept", "reject, abandon"),
    ("adult", "noun", None, None, None, None, "người lớn", "He is an adult now.", "grown-up, mature", "child, minor"),
    ("advance", "verb", "advanced", "advanced", "advancing", None, "tiến bộ, tiến lên", "She advanced to the next round.", "progress, proceed", "retreat, regress"),
    ("advanced", "adj", None, None, None, None, "tiên tiến, nâng cao", "He is in an advanced class.", "sophisticated, developed", "basic, simple"),
    ("advantage", "noun", None, None, None, None, "lợi thế, ưu điểm", "Her height is an advantage in basketball.", "benefit, edge", "disadvantage, drawback"),
    ("adventure", "noun", None, None, None, None, "cuộc phiêu lưu", "They went on an adventure in the jungle.", "expedition, journey", "caution, safety"),
    ("advertising", "noun", None, None, None, None, "quảng cáo", "Advertising helps sell products.", "promotion, marketing", "censorship, suppression"),
    ("advice", "noun", None, None, None, None, "lời khuyên", "She gave me good advice.", "counsel, guidance", "misguidance, misinformation"),
    ("advise", "verb", "advised", "advised", "advising", None, "khuyên bảo", "I advise you to study harder.", "recommend, suggest", "dissuade, discourage"),
    ("adviser", "noun", None, None, None, None, "cố vấn", "He is my academic adviser.", "counselor, mentor", "advisee, pupil"),
    ("advocate", "noun", None, None, None, None, "người ủng hộ, luật sư", "She is an advocate for human rights.", "supporter, defender", "opponent, adversary"),
    ("affair", "noun", None, None, None, None, "vấn đề, chuyện tình", "The affair was kept secret.", "matter, concern", "indifference, apathy"),
    ("affect", "verb", "affected", "affected", "affecting", None, "ảnh hưởng", "The weather affects my mood.", "influence, impact", "protect, insulate"),
    ("afford", "verb", "afforded", "afforded", "affording", None, "có đủ khả năng (chi trả)", "I can't afford a new car.", "manage, bear", "cannot, refuse"),
    ("afraid", "adj", None, None, None, None, "sợ hãi", "She is afraid of spiders.", "scared, frightened", "brave, unafraid"),
    ("African", "adj", None, None, None, None, "thuộc về châu Phi", "He is African.", "Black, African descent", "non-African, foreign"),
    ("African-American", "adj", None, None, None, None, "người Mỹ gốc Phi", "She is African-American.", "Black, Afro-American", "non-African-American, foreign"),
    ("after", "prep", None, None, None, None, "sau khi", "We went home after the party.", "following, subsequent to", "before, prior to"),
    ("afternoon", "noun", None, None, None, None, "buổi chiều", "Let's meet this afternoon.", "evening, midday", "morning, dawn"),
    ("again", "adv", None, None, None, None, "lại, một lần nữa", "Please say it again.", "once more, anew", "never, not again"),
    ("against", "prep", None, None, None, None, "chống lại, đối lập", "He is against the idea.", "opposed to, contrary to", "for, in favor of"),
    ("age", "noun", None, None, None, None, "tuổi tác", "What is your age?", "years, lifespan", "youth, childhood"),
    ("agency", "noun", None, None, None, None, "cơ quan, đại lý", "She works for a travel agency.", "organization, company", "independence, autonomy"),
    ("agenda", "noun", None, None, None, None, "chương trình nghị sự", "The agenda for the meeting is ready.", "schedule, plan", "disorganization, chaos"),
    ("agent", "noun", None, None, None, None, "đại lý, tác nhân", "He is a secret agent.", "representative, spy", "civilian, non-agent"),
    ("aggressive", "adj", None, None, None, None, "hung hăng, năng nổ", "The dog is aggressive.", "hostile, combative", "passive, peaceful"),
    ("ago", "adv", None, None, None, None, "trước đây", "I moved here two years ago.", "previously, formerly", "now, currently"),
    ("agree", "verb", "agreed", "agreed", "agreeing", None, "đồng ý", "I agree with you.", "accept, concur", "disagree, dissent"),
    ("agreement", "noun", None, None, None, None, "sự thỏa thuận", "They signed an agreement.", "contract, accord", "disagreement, dispute"),
    ("agricultural", "adj", None, None, None, None, "thuộc nông nghiệp", "Vietnam is an agricultural country.", "farming, rural", "urban, industrial"),
    ("ah", "interj", None, None, None, None, "à, ôi", "Ah, I see!", None, None),
    ("ahead", "adv", None, None, None, None, "phía trước", "Go straight ahead.", "forward, on", "backward, behind"),
    ("aid", "noun", None, None, None, None, "sự giúp đỡ, viện trợ", "He received medical aid.", "assistance, help", "hindrance, obstruction"),
    ("aide", "noun", None, None, None, None, "trợ lý", "She is a teacher's aide.", "assistant, helper", "supervisor, manager"),
    ("AIDS", "noun", None, None, None, None, "bệnh AIDS", "AIDS is a serious disease.", "HIV, immunodeficiency", "health, immunity"),
    ("aim", "verb", "aimed", "aimed", "aiming", None, "nhắm, mục tiêu", "He aimed at the target.", "intend, plan", "neglect, ignore"),
    ("air", "noun", None, None, None, None, "không khí", "The air is fresh today.", "atmosphere, breeze", "pollution, smog"),
    ("aircraft", "noun", None, None, None, None, "máy bay", "The aircraft landed safely.", "plane, jet", "drone, helicopter"),
    ("airline", "noun", None, None, None, None, "hãng hàng không", "Vietnam Airlines is a popular airline.", "carrier, flight", "ground, land"),
    ("airport", "noun", None, None, None, None, "sân bay", "We arrived at the airport.", "airfield, terminal", "station, dock"),
    ("album", "noun", None, None, None, None, "album, tập ảnh", "She bought a new album.", "collection, compilation", "single, solo"),
    ("alcohol", "noun", None, None, None, None, "rượu, cồn", "Alcohol is not allowed here.", "ethanol, liquor", "sober, teetotal"),
    ("alive", "adj", None, None, None, None, "sống, còn sống", "He is still alive.", "living, existing", "dead, deceased"),
    ("all", "pron", None, None, None, None, "tất cả", "All students must attend.", "everyone, everything", "none, nothing"),
    ("alliance", "noun", None, None, None, None, "liên minh", "The countries formed an alliance.", "union, coalition", "division, separation"),
    ("allow", "verb", "allowed", "allowed", "allowing", None, "cho phép", "They allowed us to enter.", "permit, let", "forbid, prohibit"),
    ("ally", "noun", None, None, None, None, "đồng minh", "France is an ally of the US.", "partner, supporter", "enemy, opponent"),
    ("almost", "adv", None, None, None, None, "gần như", "I almost missed the bus.", "nearly, practically", "barely, hardly"),
    ("alone", "adj", None, None, None, None, "một mình", "She lives alone.", "by oneself, solo", "together, accompanied"),
    ("along", "prep", None, None, None, None, "dọc theo", "We walked along the river.", "beside, alongside", "across, through"),
    ("already", "adv", None, None, None, None, "đã, rồi", "I have already finished my homework.", "previously, before", "not yet, still"),
    ("also", "adv", None, None, None, None, "cũng, ngoài ra", "She is smart and also kind.", "too, as well", "only, just"),
    ("alter", "verb", "altered", "altered", "altering", None, "thay đổi, biến đổi", "He altered his plans.", "change, modify", "maintain, preserve"),
    ("alternative", "noun", None, None, None, None, "sự lựa chọn thay thế", "We need an alternative solution.", "option, substitute", "same, identical"),
    ("although", "conj", None, None, None, None, "mặc dù", "Although it rained, we went out.", "though, even though", "because, since"),
    ("always", "adv", None, None, None, None, "luôn luôn", "She always wakes up early.", "forever, constantly", "never, seldom"),
    ("AM", "noun", None, None, None, None, "buổi sáng, trước trưa", "I get up at 6 AM.", "morning, dawn", "PM, evening"),
    ("amazing", "adj", None, None, None, None, "đáng kinh ngạc", "The view is amazing.", "astonishing, incredible", "unimpressive, ordinary"),
    ("American", "adj", None, None, None, None, "người Mỹ, thuộc về nước Mỹ", "He is American.", "US, American citizen", "foreign, non-American"),
    ("among", "prep", None, None, None, None, "giữa, trong số", "She is among the best students.", "between, amidst", "outside, apart"),
    ("amount", "noun", None, None, None, None, "số lượng", "The amount of money is large.", "quantity, sum", "lack, deficiency"),
    ("analysis", "noun", None, None, None, None, "sự phân tích", "The analysis was thorough.", "examination, study", "synthesis, combination"),
    ("analyst", "noun", None, None, None, None, "nhà phân tích", "He is a financial analyst.", "examiner, evaluator", "non-analyst, layman"),
    ("analyze", "verb", "analyzed", "analyzed", "analyzing", None, "phân tích", "She analyzed the data.", "examine, inspect", "ignore, overlook"),
    ("ancient", "adj", None, None, None, None, "cổ xưa", "The city has many ancient buildings.", "old, antique", "modern, new"),
    ("and", "conj", None, None, None, None, "và", "You and I are friends.", "plus, also", "but, however"),
    ("anger", "noun", None, None, None, None, "sự tức giận", "He couldn't hide his anger.", "fury, rage", "calm, peace"),
    ("angle", "noun", None, None, None, None, "góc, quan điểm", "The angle of the photo is perfect.", "perspective, viewpoint", "straight, line"),
    ("angry", "adj", None, None, None, None, "tức giận", "She was angry about the delay.", "mad, furious", "calm, pleased"),
    ("animal", "noun", None, None, None, None, "động vật", "The zoo has many animals.", "creature, beast", "human, person"),
    ("anniversary", "noun", None, None, None, None, "ngày kỷ niệm", "Today is their wedding anniversary.", "celebration, commemoration", "oblivion, forgetfulness"),
    ("announce", "verb", "announced", "announced", "announcing", None, "thông báo", "They announced the results.", "declare, proclaim", "conceal, hide"),
    ("annual", "adj", None, None, None, None, "hàng năm", "The annual meeting is in June.", "yearly, once-a-year", "monthly, weekly"),
    ("another", "pron", None, None, None, None, "khác, một cái nữa", "Can I have another piece?", "additional, one more", "same, identical"),
    ("answer", "noun", None, None, None, None, "câu trả lời", "What is your answer?", "response, reply", "question, inquiry"),
    ("anticipate", "verb", "anticipated", "anticipated", "anticipating", None, "dự đoán, mong đợi", "We anticipate good results.", "expect, predict", "doubt, question"),
    ("anxiety", "noun", None, None, None, None, "sự lo lắng", "She suffers from anxiety.", "nervousness, worry", "calm, peace"),
    ("any", "pron", None, None, None, None, "bất kỳ", "Do you have any questions?", "some, whichever", "none, no"),
    ("anybody", "pron", None, None, None, None, "bất kỳ ai", "Anybody can join the club.", "everyone, all", "nobody, none"),
    ("anymore", "adv", None, None, None, None, "nữa, không còn nữa", "I don't live there anymore.", "no longer, nowaydays", "still, yet"),
    ("anyone", "pron", None, None, None, None, "bất kỳ ai", "Anyone can do it.", "everyone, all", "nobody, none"),
    ("anything", "pron", None, None, None, None, "bất kỳ điều gì", "Is there anything I can do?", "something, whatever", "nothing, none"),
    ("anyway", "adv", None, None, None, None, "dù sao, dù thế nào", "Anyway, let's continue.", "regardless, anyhow", "nevertheless, but"),
    ("anywhere", "adv", None, None, None, None, "bất cứ nơi nào", "You can sit anywhere.", "everywhere, wherever", "nowhere, nowhere"),
    ("apart", "adv", None, None, None, None, "cách xa, riêng biệt", "They live apart now.", "separately, aside", "together, close"),
    ("apartment", "noun", None, None, None, None, "căn hộ", "She bought a new apartment.", "flat, unit", "house, villa"),
    ("apparent", "adj", None, None, None, None, "rõ ràng, hiển nhiên", "It is apparent that he is tired.", "obvious, evident", "hidden, obscure"),
    ("apparently", "adv", None, None, None, None, "hình như, rõ ràng", "Apparently, she is not coming.", "seemingly, evidently", "concealed, hidden"),
    ("appeal", "verb", "appealed", "appealed", "appealing", None, "kêu gọi, hấp dẫn", "The ad appeals to young people.", "attract, charm", "repel, disgust"),
    ("appear", "verb", "appeared", "appeared", "appearing", None, "xuất hiện", "He appeared suddenly.", "emerge, show up", "disappear, vanish"),
    ("appearance", "noun", None, None, None, None, "diện mạo, sự xuất hiện", "Her appearance changed a lot.", "look, semblance", "disappearance, invisibility"),
    ("apple", "noun", None, None, None, None, "quả táo", "I eat an apple every day.", "fruit, malus pumila", "vegetable, non-fruit"),
    ("application", "noun", None, None, None, None, "đơn xin, ứng dụng", "I submitted my application.", "form, request", "rejection, denial"),
    ("apply", "verb", "applied", "applied", "applying", None, "nộp, áp dụng", "She applied for a job.", "submit, send in", "withdraw, retract"),
    ("appoint", "verb", "appointed", "appointed", "appointing", None, "bổ nhiệm, chỉ định", "He was appointed manager.", "assign, designate", "dismiss, remove"),
    ("appointment", "noun", None, None, None, None, "cuộc hẹn, sự bổ nhiệm", "I have a doctor's appointment.", "meeting, engagement", "cancellation, postponement"),
    ("appreciate", "verb", "appreciated", "appreciated", "appreciating", None, "đánh giá cao, cảm kích", "I appreciate your help.", "value, cherish", "disregard, overlook"),
    ("approach", "verb", "approached", "approached", "approaching", None, "tiếp cận, phương pháp", "She approached the problem carefully.", "address, tackle", "avoid, ignore"),
    ("appropriate", "adj", None, None, None, None, "thích hợp, phù hợp", "This is the appropriate solution.", "suitable, fitting", "inappropriate, unsuitable"),
    ("approval", "noun", None, None, None, None, "sự chấp thuận", "He received approval for his plan.", "acceptance, endorsement", "rejection, denial"),
    ("approve", "verb", "approved", "approved", "approving", None, "chấp thuận, phê duyệt", "They approved the proposal.", "accept, endorse", "reject, deny"),
    ("approximately", "adv", None, None, None, None, "xấp xỉ, khoảng", "There are approximately 100 people.", "about, around", "exactly, precisely"),
    ("Arab", "noun", None, None, None, None, "người Ả Rập", "He is an Arab.", "Arabic, Middle Eastern", "non-Arab, foreign"),
    ("architect", "noun", None, None, None, None, "kiến trúc sư", "She is an architect.", "designer, planner", "builder, laborer"),
    ("area", "noun", None, None, None, None, "khu vực, diện tích", "This area is very quiet.", "region, zone", "noise, disturbance"),
    ("argue", "verb", "argued", "argued", "arguing", None, "tranh luận, cãi nhau", "They argued about money.", "dispute, debate", "agree, concur"),
    ("argument", "noun", None, None, None, None, "cuộc tranh luận, lý lẽ", "The argument lasted for hours.", "dispute, debate", "agreement, harmony"),
    ("arise", "verb", "arose", "arisen", "arising", None, "phát sinh, nảy sinh", "Problems may arise.", "occur, happen", "cease, stop"),
    ("arm", "noun", None, None, None, None, "cánh tay", "He broke his arm.", "limb, appendage", "torso, body"),
    ("armed", "adj", None, None, None, None, "vũ trang", "The police are armed.", "equipped, fortified", "unarmed, defenseless"),
    ("army", "noun", None, None, None, None, "quân đội", "He joined the army.", "military, forces", "civilian, non-combatant"),
    ("around", "adv", None, None, None, None, "xung quanh, khoảng", "There are many shops around here.", "nearby, close", "far, distant"),
    ("arrange", "verb", "arranged", "arranged", "arranging", None, "sắp xếp, tổ chức", "She arranged the meeting.", "organize, set up", "disorganize, cancel"),
    ("arrangement", "noun", None, None, None, None, "sự sắp xếp, sự tổ chức", "The arrangement was perfect.", "organization, setup", "disorganization, chaos"),
    ("arrest", "verb", "arrested", "arrested", "arresting", None, "bắt giữ", "The police arrested the suspect.", "capture, detain", "release, free"),
    ("arrival", "noun", None, None, None, None, "sự đến, sự xuất hiện", "Her arrival surprised everyone.", "coming, appearance", "departure, leaving"),
    ("arrive", "verb", "arrived", "arrived", "arriving", None, "đến, tới", "They arrived late.", "reach, get to", "depart, leave"),
    ("art", "noun", None, None, None, None, "nghệ thuật", "She loves modern art.", "craft, skill", "ignorance, ineptitude"),
    ("article", "noun", None, None, None, None, "bài báo, vật phẩm", "I read an interesting article.", "piece, item", "whole, entirety"),
    ("artist", "noun", None, None, None, None, "nghệ sĩ, họa sĩ", "He is a famous artist.", "painter, sculptor", "non-artist, amateur"),
    ("artistic", "adj", None, None, None, None, "có tính nghệ thuật", "She has artistic talent.", "creative, imaginative", "unartistic, mundane"),
    ("as", "conj", None, None, None, None, "như, khi", "As I said before, be careful.", "like, as if", "unlike, different from"),
    ("Asian", "adj", None, None, None, None, "người châu Á, thuộc về châu Á", "She is Asian.", "Oriental, Asian descent", "non-Asian, foreign"),
    ("aside", "adv", None, None, None, None, "sang một bên, để dành", "He put money aside for a trip.", "apart, away", "together, with"),
    ("ask", "verb", "asked", "asked", "asking", None, "hỏi, yêu cầu", "She asked a question.", "inquire, request", "answer, respond"),
    ("asleep", "adj", None, None, None, None, "đang ngủ", "The baby is asleep.", "sleeping, napping", "awake, alert"),
    ("aspect", "noun", None, None, None, None, "khía cạnh", "This aspect is important.", "facet, feature", "whole, entirety"),
    ("assault", "noun", None, None, None, None, "cuộc tấn công, hành hung", "He was charged with assault.", "attack, battery", "defense, protection"),
    ("assert", "verb", "asserted", "asserted", "asserting", None, "khẳng định, xác nhận", "He asserted his innocence.", "declare, maintain", "deny, reject"),
    ("assess", "verb", "assessed", "assessed", "assessing", None, "đánh giá", "The teacher assessed the students.", "evaluate, appraise", "ignore, neglect"),
    ("assessment", "noun", None, None, None, None, "sự đánh giá", "The assessment was fair.", "evaluation, appraisal", "neglect, disregard"),
    ("asset", "noun", None, None, None, None, "tài sản, lợi thế", "Her experience is an asset.", "advantage, benefit", "liability, disadvantage"),
    ("assign", "verb", "assigned", "assigned", "assigning", None, "phân công, chỉ định", "He was assigned a new task.", "allocate, designate", "withdraw, remove"),
    ("assignment", "noun", None, None, None, None, "bài tập, nhiệm vụ", "I finished my assignment.", "task, duty", "neglect, ignore"),
    ("assist", "verb", "assisted", "assisted", "assisting", None, "hỗ trợ, giúp đỡ", "He assisted me with my homework.", "help, aid", "hinder, obstruct"),
    ("assistance", "noun", None, None, None, None, "sự giúp đỡ, hỗ trợ", "She asked for assistance.", "help, support", "hindrance, obstruction"),
    ("assistant", "noun", None, None, None, None, "trợ lý, phụ tá", "He is a shop assistant.", "aide, helper", "manager, supervisor"),
    ("associate", "verb", "associated", "associated", "associating", None, "liên kết, kết hợp", "She associated the smell with flowers.", "link, connect", "separate, disconnect"),
    ("association", "noun", None, None, None, None, "hiệp hội, sự liên kết", "He joined the association.", "organization, club", "disassociation, separation"),
    ("assume", "verb", "assumed", "assumed", "assuming", None, "giả định, cho rằng", "I assume you are ready.", "presume, suppose", "doubt, question"),
    ("assumption", "noun", None, None, None, None, "giả định, giả thiết", "The assumption was incorrect.", "premise, hypothesis", "fact, reality"),
    ("assure", "verb", "assured", "assured", "assuring", None, "đảm bảo, cam đoan", "He assured me of his support.", "guarantee, promise", "doubt, question"),
    ("at", "prep", None, None, None, None, "tại, ở", "She is at home.", "in, on", "away, out"),
    ("athlete", "noun", None, None, None, None, "vận động viên", "He is a professional athlete.", "sportsperson, competitor", "non-athlete, spectator"),
    ("athletic", "adj", None, None, None, None, "thuộc thể thao, khỏe mạnh", "She has an athletic build.", "fit, sporty", "unathletic, weak"),
    ("atmosphere", "noun", None, None, None, None, "không khí, bầu không khí", "The atmosphere was tense.", "ambiance, mood", "vacuum, emptiness"),
    ("attach", "verb", "attached", "attached", "attaching", None, "gắn, đính kèm", "Please attach the file.", "join, connect", "detach, disconnect"),
    ("attack", "verb", "attacked", "attacked", "attacking", None, "tấn công", "The army attacked at dawn.", "assault, strike", "defend, protect"),
    ("attempt", "verb", "attempted", "attempted", "attempting", None, "cố gắng, thử", "He attempted to solve the problem.", "try, endeavor", "give up, quit"),
    ("attend", "verb", "attended", "attended", "attending", None, "tham dự, chú ý", "She attended the meeting.", "participate, attend to", "ignore, overlook"),
    ("attention", "noun", None, None, None, None, "sự chú ý", "Pay attention to the instructions.", "notice, awareness", "inattention, disregard"),
    ("attitude", "noun", None, None, None, None, "thái độ", "Her attitude is positive.", "mindset, outlook", "negativity, pessimism"),
    ("attorney", "noun", None, None, None, None, "luật sư", "He is an attorney.", "lawyer, counselor", "client, defendant"),
    ("attract", "verb", "attracted", "attracted", "attracting", None, "thu hút, hấp dẫn", "The show attracted many viewers.", "draw, entice", "repel, deter"),
    ("attractive", "adj", None, None, None, None, "hấp dẫn, lôi cuốn", "She is very attractive.", "appealing, charming", "unattractive, repulsive"),
    ("attribute", "noun", None, None, None, None, "thuộc tính, đặc điểm", "Honesty is a good attribute.", "trait, quality", "flaw, defect"),
    ("audience", "noun", None, None, None, None, "khán giả", "The audience applauded.", "viewers, spectators", "performers, actors"),
    ("author", "noun", None, None, None, None, "tác giả", "He is the author of the book.", "writer, creator", "reader, audience"),
    ("authority", "noun", None, None, None, None, "quyền lực, nhà chức trách", "He has authority over the staff.", "power, control", "subordination, obedience"),
    ("auto", "noun", None, None, None, None, "ô tô, xe hơi", "He bought a new auto.", "car, vehicle", "bicycle, pedestrian"),
    ("available", "adj", None, None, None, None, "có sẵn, sẵn sàng", "The book is available now.", "accessible, obtainable", "unavailable, inaccessible"),
    ("average", "adj", None, None, None, None, "trung bình", "Her grades are above average.", "mean, median", "exceptional, outstanding"),
    ("avoid", "verb", "avoided", "avoided", "avoiding", None, "tránh, tránh xa", "He avoided the puddle.", "dodge, evade", "confront, face"),
    ("award", "noun", None, None, None, None, "giải thưởng", "She won an award.", "prize, accolade", "penalty, punishment"),
    ("aware", "adj", None, None, None, None, "nhận thức, biết", "He is aware of the risks.", "conscious, cognizant", "unaware, ignorant"),
    ("awareness", "noun", None, None, None, None, "sự nhận thức", "Awareness of health is important.", "consciousness, recognition", "ignorance, oblivion"),
    ("away", "adv", None, None, None, None, "xa, đi xa", "She moved away last year.", "afar, yonder", "near, close"),
    ("awful", "adj", None, None, None, None, "kinh khủng, tồi tệ", "The weather is awful today.", "terrible, dreadful", "pleasant, nice"),
    ("baby", "noun", None, None, None, None, "em bé", "The baby is sleeping.", "infant, newborn", "adult, elder"),
    ("back", "noun", None, None, None, None, "lưng, phía sau", "He hurt his back.", "rear, spine", "front, chest"),
    ("background", "noun", None, None, None, None, "nền, lý lịch", "She has a strong academic background.", "history, experience", "foreground, front"),
    ("bad", "adj", None, None, None, None, "xấu, tồi", "The food tastes bad.", "poor, awful", "good, excellent"),
    ("badly", "adv", None, None, None, None, "tệ, dở", "He sings badly.", "poorly, inadequately", "well, adequately"),
    ("bag", "noun", None, None, None, None, "túi, bao", "She bought a new bag.", "sack, purse", "basket, container"),
    ("bake", "verb", "baked", "baked", "baking", None, "nướng, làm bánh", "She baked a cake.", "cook, prepare", "burn, spoil"),
    ("balance", "noun", None, None, None, None, "cân bằng, số dư", "He lost his balance.", "stability, equilibrium", "imbalance, instability"),
    ("ball", "noun", None, None, None, None, "quả bóng", "The ball is round.", "sphere, orb", "cube, square"),
    ("ban", "verb", "banned", "banned", "banning", None, "cấm, lệnh cấm", "Smoking is banned here.", "prohibit, forbid", "allow, permit"),
    ("band", "noun", None, None, None, None, "ban nhạc, dải", "He plays in a band.", "musical group, ensemble", "solo, individual"),
    ("bank", "noun", None, None, None, None, "ngân hàng, bờ", "She works at a bank.", "financial institution, depository", "withdraw, remove"),
    ("bar", "noun", None, None, None, None, "quán bar, thanh", "We met at the bar.", "pub, tavern", "restaurant, cafe"),
    ("barely", "adv", None, None, None, None, "hầu như không", "He barely passed the exam.", "hardly, scarcely", "easily, comfortably"),
    ("barrel", "noun", None, None, None, None, "thùng, ống", "The barrel is full of oil.", "cask, drum", "empty, void"),
    ("barrier", "noun", None, None, None, None, "rào cản, chướng ngại", "Language is a barrier.", "obstacle, hurdle", "aid, assistance"),
    ("base", "noun", None, None, None, None, "cơ sở, nền tảng", "The base of the statue is wide.", "foundation, basis", "tip, apex"),
    ("baseball", "noun", None, None, None, None, "bóng chày", "He likes to play baseball.", "bat-and-ball game, sport", "football, basketball"),
    ("basic", "adj", None, None, None, None, "cơ bản, đơn giản", "She has basic knowledge.", "fundamental, elementary", "advanced, complex"),
    ("basically", "adv", None, None, None, None, "về cơ bản", "Basically, it's a good idea.", "essentially, fundamentally", "superficially, apparently"),
    ("basis", "noun", None, None, None, None, "nền tảng, căn cứ", "The basis of the theory is sound.", "foundation, groundwork", "superstructure, consequence"),
    ("basket", "noun", None, None, None, None, "giỏ, rổ", "She put apples in the basket.", "container, receptacle", "empty, void"),
    ("basketball", "noun", None, None, None, None, "bóng rổ", "He plays basketball every weekend.", "hoop, net game", "football, baseball"),
    ("bathroom", "noun", None, None, None, None, "phòng tắm", "The bathroom is clean.", "washroom, restroom", "kitchen, bedroom"),
    ("battery", "noun", None, None, None, None, "pin, ắc quy", "My phone's battery is low.", "accumulator, power source", "drain, depletion"),
    ("battle", "noun", None, None, None, None, "trận chiến, cuộc chiến", "The battle lasted for hours.", "fight, conflict", "peace, truce"),
    ("be", "verb", "was/were", "been", "being", None, "là, thì, ở", "She wants to be a doctor.", "exist, live", "cease, die"),
    ("beach", "noun", None, None, None, None, "bãi biển", "We went to the beach.", "shore, coastline", "mountain, desert"),
    ("bean", "noun", None, None, None, None, "đậu, hạt đậu", "She likes green beans.", "legume, seed", "animal, vegetable"),
    ("bear", "verb", "bore", "borne", "bearing", None, "mang, chịu đựng", "She can't bear the pain.", "endure, tolerate", "avoid, escape"),
    ("beat", "verb", "beat", "beaten", "beating", None, "đánh, nhịp", "He beat the drum.", "strike, hit", "lose, surrender"),
    ("beautiful", "adj", None, None, None, None, "đẹp, xinh đẹp", "She is a beautiful girl.", "pretty, lovely", "ugly, unattractive"),
    ("beauty", "noun", None, None, None, None, "vẻ đẹp", "The beauty of nature is amazing.", "attractiveness, charm", "ugliness, deformity"),
    ("because", "conj", None, None, None, None, "bởi vì", "I stayed home because it rained.", "since, as", "although, but"),
    ("become", "verb", "became", "become", "becoming", None, "trở thành", "He became a teacher.", "turn into, transform", "remain, stay"),
    ("bed", "noun", None, None, None, None, "giường", "The bed is comfortable.", "bedding, mattress", "floor, ceiling"),
    ("bedroom", "noun", None, None, None, None, "phòng ngủ", "Her bedroom is large.", "sleeping room, chamber", "living room, kitchen"),
    ("beer", "noun", None, None, None, None, "bia", "He drank a glass of beer.", "lager, ale", "whiskey, vodka"),
    ("before", "prep", None, None, None, None, "trước khi", "Wash your hands before eating.", "prior to, ahead of", "after, following"),
    ("begin", "verb", "began", "begun", "beginning", None, "bắt đầu", "The show will begin soon.", "start, commence", "end, finish"),
    ("beginning", "noun", None, None, None, None, "sự bắt đầu, phần đầu", "The beginning of the story is interesting.", "start, commencement", "end, conclusion"),
    ("behavior", "noun", None, None, None, None, "hành vi, cách cư xử", "His behavior is strange.", "conduct, demeanor", "misconduct, bad behavior"),
    ("behind", "prep", None, None, None, None, "phía sau, đằng sau", "The cat is behind the door.", "at the back of, in the rear of", "in front of, ahead of"),
    ("being", "noun", None, None, None, None, "sự tồn tại, sinh vật", "Human beings are complex.", "creature, organism", "inanimate, non-living"),
    ("belief", "noun", None, None, None, None, "niềm tin, tín ngưỡng", "Her belief is strong.", "faith, conviction", "disbelief, skepticism"),
    ("believe", "verb", "believed", "believed", "believing", None, "tin tưởng", "I believe in you.", "trust, have faith in", "doubt, disbelieve"),
    ("bell", "noun", None, None, None, None, "chuông", "The bell rang loudly.", "chime, toll", "silence, quiet"),
    ("belong", "verb", "belonged", "belonged", "belonging", None, "thuộc về", "This book belongs to me.", "be owned by, be a part of", "be alien to, dissociate from"),
    ("below", "prep", None, None, None, None, "bên dưới, thấp hơn", "The temperature is below zero.", "under, beneath", "above, over"),
    ("belt", "noun", None, None, None, None, "thắt lưng, dây nịt", "He wears a black belt.", "strap, sash", "loose, unbelted"),
    ("bench", "noun", None, None, None, None, "ghế dài", "They sat on the bench.", "seat, pew", "stand, table"),
    ("bend", "verb", "bent", "bent", "bending", None, "uốn cong, cúi xuống", "He bent down to pick up the coin.", "curve, flex", "straighten, unbend"),
    ("beneath", "prep", None, None, None, None, "bên dưới, thấp hơn", "The ground beneath our feet.", "under, below", "above, over"),
    ("benefit", "noun", None, None, None, None, "lợi ích, phúc lợi", "Exercise has many benefits.", "advantage, profit", "disadvantage, drawback"),
    ("beside", "prep", None, None, None, None, "bên cạnh", "She sat beside me.", "next to, alongside", "far from, apart"),
    ("besides", "adv", None, None, None, None, "ngoài ra, bên cạnh đó", "Besides English, she speaks French.", "in addition, furthermore", "excluding, apart from"),
    ("best", "adj", None, None, None, None, "tốt nhất", "She is my best friend.", "finest, greatest", "worst, least"),
    ("bet", "verb", "bet", "bet", "betting", None, "cá cược, đặt cược", "He bet on the winning horse.", "wager, stake", "lose, forfeit"),
    ("better", "adj", None, None, None, None, "tốt hơn", "This solution is better.", "superior, improved", "inferior, worse"),
    ("between", "prep", None, None, None, None, "giữa, ở giữa", "The ball is between the boxes.", "among, in the middle of", "outside, apart"),
    ("beyond", "prep", None, None, None, None, "vượt ra ngoài, ngoài", "The house is beyond the river.", "past, over", "before, in front of"),
    ("Bible", "noun", None, None, None, None, "Kinh Thánh", "He reads the Bible every day.", "scripture, holy book", "secular, non-religious"),
    ("big", "adj", None, None, None, None, "lớn, to", "The elephant is big.", "huge, large", "small, tiny"),
    ("bike", "noun", None, None, None, None, "xe đạp", "She rides her bike to school.", "bicycle, cycle", "motorcycle, car"),
    ("bill", "noun", None, None, None, None, "hóa đơn, dự luật", "He paid the bill.", "invoice, statement", "receipt, payment"),
    ("billion", "noun", None, None, None, None, "tỷ", "The company is worth a billion dollars.", "thousand million, 10^9", "million, 10^6"),
    ("bind", "verb", "bound", "bound", "binding", None, "buộc, trói, ràng buộc", "He bound the books together.", "tie, fasten", "loosen, unbind"),
    ("biological", "adj", None, None, None, None, "sinh học, thuộc về sinh học", "She studies biological sciences.", "life science, organic", "physical, inorganic"),
    ("bird", "noun", None, None, None, None, "chim", "The bird is singing.", "avian, creature", "mammal, reptile"),
    ("birth", "noun", None, None, None, None, "sự sinh ra, sự ra đời", "The birth of a child is special.", "delivery, nativity", "death, demise"),
    ("birthday", "noun", None, None, None, None, "ngày sinh nhật", "Her birthday is in May.", "anniversary, celebration", "deathday, memorial"),
    ("bit", "noun", None, None, None, None, "một chút, phần nhỏ", "I need a bit of help.", "small amount, piece", "lot, whole"),
    ("bite", "verb", "bit", "bitten", "biting", None, "cắn, ngoạm", "The dog bit my hand.", "chew, gnaw", "lick, soothe"),
    ("black", "adj", None, None, None, None, "màu đen", "She wears a black dress.", "dark, ebony", "white, colorless"),
    ("blade", "noun", None, None, None, None, "lưỡi (dao, kiếm)", "The blade is sharp.", "edge, cutter", "dull, blunt"),
    ("blame", "verb", "blamed", "blamed", "blaming", None, "đổ lỗi, trách", "Don't blame me for the mistake.", "accuse, hold responsible", "absolve, exonerate"),
    ("blanket", "noun", None, None, None, None, "chăn, mền", "He covered himself with a blanket.", "cover, quilt", "uncover, expose"),
    ("blind", "adj", None, None, None, None, "mù, không nhìn thấy", "He is blind in one eye.", "sightless, visually impaired", "seeing, sighted"),
    ("block", "noun", None, None, None, None, "khối, tảng, dãy nhà", "She lives on this block.", "section, segment", "whole, entirety"),
    ("blood", "noun", None, None, None, None, "máu", "Blood is red.", "hemolymph, plasma", "lymph, serum"),
    ("blow", "verb", "blew", "blown", "blowing", None, "thổi, cú đánh", "The wind blows strongly.", "gust, breeze", "calm, stillness"),
    ("blue", "adj", None, None, None, None, "màu xanh dương", "The sky is blue.", "azure, cerulean", "red, green"),
    ("board", "noun", None, None, None, None, "bảng, tấm ván", "Write your name on the board.", "plank, sheet", "ignore, overlook"),
    ("boat", "noun", None, None, None, None, "thuyền, tàu", "We went fishing on a boat.", "vessel, craft", "land, shore"),
    ("body", "noun", None, None, None, None, "cơ thể, thân thể", "The human body is complex.", "physique, form", "soul, spirit"),
    ("bomb", "noun", None, None, None, None, "bom", "The bomb exploded.", "explosive, device", "peace, truce"),
    ("bombing", "noun", None, None, None, None, "sự ném bom", "The bombing caused damage.", "air raid, attack", "peace, truce"),
    ("bond", "noun", None, None, None, None, "mối liên kết, trái phiếu", "They have a strong bond.", "connection, tie", "separation, disconnection"),
    ("bone", "noun", None, None, None, None, "xương", "He broke a bone in his leg.", "ossicle, skeletal", "cartilage, tissue"),
    ("book", "noun", None, None, None, None, "sách", "I am reading a book.", "volume, tome", "scroll, manuscript"),
    ("boom", "noun", None, None, None, None, "bùng nổ, sự tăng vọt", "There was an economic boom.", "expansion, growth", "bust, recession"),
    ("boot", "noun", None, None, None, None, "giày ống, khởi động", "He wears boots in winter.", "footwear, galosh", "sandal, slipper"),
    ("border", "noun", None, None, None, None, "biên giới, mép", "They crossed the border.", "boundary, frontier", "center, middle"),
    ("born", "adj", None, None, None, None, "sinh ra, ra đời", "He was born in Hanoi.", "delivered, brought forth", "still, unborn"),
    ("borrow", "verb", "borrowed", "borrowed", "borrowing", None, "mượn, vay", "Can I borrow your pen?", "loan, rent", "lend, give"),
    ("boss", "noun", None, None, None, None, "sếp, ông chủ", "My boss is strict.", "employer, manager", "employee, worker"),
    ("both", "pron", None, None, None, None, "cả hai", "Both answers are correct.", "the two, each", "neither, none"),
    ("bother", "verb", "bothered", "bothered", "bothering", None, "làm phiền, quấy rầy", "Don't bother me now.", "disturb, interrupt", "ignore, overlook"),
    ("bottle", "noun", None, None, None, None, "chai, lọ", "She bought a bottle of water.", "container, flask", "cup, glass"),
    ("bottom", "noun", None, None, None, None, "đáy, phía dưới", "The ball is at the bottom of the box.", "base, foundation", "top, surface"),
    ("boundary", "noun", None, None, None, None, "ranh giới, giới hạn", "The fence marks the boundary.", "border, limit", "center, middle"),
    ("bowl", "noun", None, None, None, None, "bát, tô", "He ate a bowl of soup.", "dish, container", "plate, tray"),
    ("box", "noun", None, None, None, None, "hộp, cái hộp", "Put the shoes in the box.", "container, case", "open, unpacked"),
    ("boy", "noun", None, None, None, None, "cậu bé", "The boy is playing outside.", "lad, youth", "girl, woman"),
    ("boyfriend", "noun", None, None, None, None, "bạn trai", "Her boyfriend is very kind.", "partner, significant other", "girlfriend, ex-boyfriend"),
    ("brain", "noun", None, None, None, None, "não, trí tuệ", "The human brain is powerful.", "mind, intellect", "ignorance, stupidity"),
    ("branch", "noun", None, None, None, None, "cành cây, chi nhánh", "The bird sat on a branch.", "limb, bough", "trunk, root"),
    ("brand", "noun", None, None, None, None, "nhãn hiệu, thương hiệu", "This is a famous brand.", "label, trademark", "generic, unbranded"),
    ("bread", "noun", None, None, None, None, "bánh mì", "She bought fresh bread.", "loaf, baguette", "pastry, cake"),
    ("break", "verb", "broke", "broken", "breaking", None, "làm vỡ, nghỉ", "He broke the glass.", "shatter, fracture", "fix, repair"),
    ("breakfast", "noun", None, None, None, None, "bữa sáng", "I had eggs for breakfast.", "morning meal, brunch", "lunch, dinner"),
    ("breast", "noun", None, None, None, None, "ngực, vú", "She felt pain in her breast.", "chest, bosom", "back, abdomen"),
    ("breath", "noun", None, None, None, None, "hơi thở", "Take a deep breath.", "inhalation, exhalation", "suspension, cessation"),
    ("breathe", "verb", "breathed", "breathed", "breathing", None, "thở", "She can't breathe well.", "inhale, exhale", "suffocate, choke"),
    ("brick", "noun", None, None, None, None, "gạch", "The wall is made of bricks.", "block, tile", "mortar, cement"),
    ("bridge", "noun", None, None, None, None, "cầu", "They crossed the bridge.", "viaduct, overpass", "road, path"),
    ("brief", "adj", None, None, None, None, "ngắn gọn, vắn tắt", "He gave a brief explanation.", "concise, short", "long, detailed"),
    ("briefly", "adv", None, None, None, None, "một cách ngắn gọn", "She spoke briefly.", "concisely, in short", "lengthily, in detail"),
    ("bright", "adj", None, None, None, None, "sáng, thông minh", "The room is bright.", "luminous, radiant", "dim, dull"),
    ("brilliant", "adj", None, None, None, None, "xuất sắc, rực rỡ", "She is a brilliant student.", "excellent, outstanding", "mediocre, average"),
    ("bring", "verb", "brought", "brought", "bringing", None, "mang, đem lại", "Please bring your book.", "fetch, carry", "take, leave"),
    ("British", "adj", None, None, None, None, "người Anh, thuộc về nước Anh", "He is British.", "English, UK", "American, foreign"),
    ("broad", "adj", None, None, None, None, "rộng, bao quát", "The street is broad.", "wide, spacious", "narrow, tight"),
    ("broken", "adj", None, None, None, None, "bị vỡ, hỏng", "The window is broken.", "damaged, shattered", "intact, whole"),
    ("brother", "noun", None, None, None, None, "anh trai, em trai", "My brother is older than me.", "sibling, bro", "sister, cousin"),
    ("brown", "adj", None, None, None, None, "màu nâu", "She has brown hair.", "chestnut, brunette", "blonde, black"),
    ("brush", "noun", None, None, None, None, "bàn chải, cọ", "Use a brush to clean your teeth.", "cleaning tool, applicator", "sponge, cloth"),
    ("buck", "noun", None, None, None, None, "đô la, con hươu đực", "He paid five bucks for lunch.", "dollar, currency", "cent, penny"),
    ("budget", "noun", None, None, None, None, "ngân sách, ngân quỹ", "The budget is limited.", "financial plan, allocation", "debt, deficit"),
    ("build", "verb", "built", "built", "building", None, "xây dựng", "They build houses.", "construct, erect", "demolish, destroy"),
    ("building", "noun", None, None, None, None, "tòa nhà, công trình", "The building is tall.", "structure, edifice", "demolition, destruction"),
    ("bullet", "noun", None, None, None, None, "viên đạn", "The bullet hit the target.", "projectile, missile", "shield, protection"),
    ("bunch", "noun", None, None, None, None, "bó, chùm, nhóm", "She bought a bunch of flowers.", "cluster, bouquet", "single, individual"),
    ("burden", "noun", None, None, None, None, "gánh nặng", "He carries a heavy burden.", "load, weight", "relief, assistance"),
    ("burn", "verb", "burned", "burned", "burning", None, "đốt cháy, bị bỏng", "He burned his hand.", "scorch, singe", "freeze, cool"),
    ("bury", "verb", "buried", "buried", "burying", None, "chôn, mai táng", "They buried the treasure.", "inter, entomb", "exhume, uncover"),
    ("bus", "noun", None, None, None, None, "xe buýt", "I take the bus to work.", "coach, transit", "car, bike"),
    ("business", "noun", None, None, None, None, "kinh doanh, doanh nghiệp", "He owns a business.", "company, firm", "hobby, pastime"),
    ("busy", "adj", None, None, None, None, "bận rộn", "She is busy today.", "occupied, engaged", "free, available"),
    ("but", "conj", None, None, None, None, "nhưng", "I like tea but not coffee.", "however, yet", "and, also"),
    ("butter", "noun", None, None, None, None, "bơ", "She spread butter on her bread.", "margarine, spread", "jam, jelly"),
    ("button", "noun", None, None, None, None, "nút, cúc áo", "Press the button to start.", "switch, control", "lever, handle"),
    ("buy", "verb", "bought", "bought", "buying", None, "mua", "She bought a new dress.", "purchase, acquire", "sell, dispose"),
    ("buyer", "noun", None, None, None, None, "người mua", "The buyer paid in cash.", "purchaser, client", "seller, vendor"),
    ("by", "prep", None, None, None, None, "bởi, bằng, gần", "The book was written by her.", "via, through", "near, at"),
    ("cabin", "noun", None, None, None, None, "túp lều, phòng nhỏ", "They stayed in a cabin by the lake.", "chalet, lodge", "mansion, hotel"),
    ("cabinet", "noun", None, None, None, None, "tủ, nội các", "The cabinet is made of wood.", "cupboard, closet", "open, empty"),
    ("cable", "noun", None, None, None, None, "dây cáp, dây điện", "Connect the cable to the TV.", "wire, cord", "wireless, Bluetooth"),
    ("cake", "noun", None, None, None, None, "bánh ngọt", "She baked a chocolate cake.", "dessert, pastry", "bread, biscuit"),
    ("calculate", "verb", "calculated", "calculated", "calculating", None, "tính toán", "He calculated the total cost.", "compute, reckon", "estimate, guess"),
    ("call", "verb", "called", "called", "calling", None, "gọi, gọi điện", "She called her friend.", "ring, contact", "ignore, neglect"),
    ("camera", "noun", None, None, None, None, "máy ảnh", "He bought a new camera.", "photographic device, camcorder", "phone, computer"),
    ("camp", "noun", None, None, None, None, "trại, cắm trại", "The children went to summer camp.", "outdoor activity, campsite", "indoor, home"),
    ("campaign", "noun", None, None, None, None, "chiến dịch", "They launched a new campaign.", "initiative, drive", "apathy, indifference"),
    ("campus", "noun", None, None, None, None, "khuôn viên trường", "The campus is very large.", "college grounds, university", "off-campus, outside"),
    ("can", "verb", "could", "could", "can", None, "có thể, biết", "She can swim well.", "be able to, capable of", "cannot, unable"),
    ("Canadian", "adj", None, None, None, None, "người Canada, thuộc về Canada", "He is Canadian.", "from Canada, Canadian citizen", "non-Canadian, foreign"),
    ("cancer", "noun", None, None, None, None, "bệnh ung thư", "She is fighting cancer.", "malignancy, tumor", "health, wellness"),
    ("candidate", "noun", None, None, None, None, "ứng viên, thí sinh", "There are five candidates for the job.", "applicant, contender", "incumbent, non-candidate"),
    ("cap", "noun", None, None, None, None, "mũ lưỡi trai, nắp", "He wore a blue cap.", "hat, headwear", "none, bare"),
    ("capability", "noun", None, None, None, None, "khả năng, năng lực", "She has great capability.", "ability, capacity", "inability, incapacity"),
    ("capable", "adj", None, None, None, None, "có khả năng, giỏi", "He is capable of solving problems.", "competent, able", "incapable, incompetent"),
    ("capacity", "noun", None, None, None, None, "sức chứa, năng lực", "The stadium has a large capacity.", "volume, size", "inability, incapacity"),
    ("capital", "noun", None, None, None, None, "thủ đô, vốn", "Hanoi is the capital of Vietnam.", "city, metropolis", "province, district"),
    ("captain", "noun", None, None, None, None, "đội trưởng, thuyền trưởng", "He is the captain of the team.", "leader, commander", "follower, subordinate"),
    ("capture", "verb", "captured", "captured", "capturing", None, "bắt giữ, chiếm lấy", "The police captured the thief.", "catch, apprehend", "release, let go"),
    ("car", "noun", None, None, None, None, "xe ô tô", "She drives a red car.", "automobile, vehicle", "bicycle, pedestrian"),
    ("carbon", "noun", None, None, None, None, "cacbon, than", "Carbon is a chemical element.", "element, graphite", "non-carbon, inorganic"),
    ("card", "noun", None, None, None, None, "thẻ, thiệp", "He gave her a birthday card.", "greeting card, postcard", "letter, bill"),
    ("care", "noun", None, None, None, None, "sự chăm sóc, quan tâm", "She takes care of her grandmother.", "attention, concern", "neglect, indifference"),
    ("career", "noun", None, None, None, None, "nghề nghiệp, sự nghiệp", "He chose a career in medicine.", "profession, occupation", "hobby, pastime"),
    ("careful", "adj", None, None, None, None, "cẩn thận, chu đáo", "Be careful when crossing the street.", "cautious, attentive", "careless, reckless"),
    ("carefully", "adv", None, None, None, None, "một cách cẩn thận", "She read the instructions carefully.", "attentively, meticulously", "carelessly, hastily"),
    ("carrier", "noun", None, None, None, None, "người vận chuyển, hãng vận tải", "The carrier delivered the package.", "transporter, deliverer", "receiver, addressee"),
    ("carry", "verb", "carried", "carried", "carrying", None, "mang, vác", "He carried the box upstairs.", "lift, tote", "drop, abandon"),
    ("case", "noun", None, None, None, None, "trường hợp, hộp", "This is a special case.", "instance, example", "general, rule"),
    ("cash", "noun", None, None, None, None, "tiền mặt", "He paid in cash.", "currency, money", "credit, debit"),
    ("cast", "verb", "cast", "cast", "casting", None, "ném, đúc, tuyển chọn", "She cast her vote.", "throw, fling", "catch, receive"),
    ("cat", "noun", None, None, None, None, "con mèo", "The cat is sleeping.", "feline, kitty", "dog, canine"),
    ("catch", "verb", "caught", "caught", "catching", None, "bắt, đón", "He caught the ball.", "grab, seize", "miss, lose"),
    ("category", "noun", None, None, None, None, "loại, hạng mục", "This product is in a new category.", "class, type", "individual, outlier"),
    ("Catholic", "adj", None, None, None, None, "người Công giáo, thuộc Công giáo", "She is Catholic.", "Christian, believer", "non-Catholic, atheist"),
    ("cause", "noun", None, None, None, None, "nguyên nhân, lý do", "The cause of the fire is unknown.", "reason, source", "effect, result"),
    ("ceiling", "noun", None, None, None, None, "trần nhà", "The ceiling is painted white.", "roof, overhead", "floor, ground"),
    ("celebrate", "verb", "celebrated", "celebrated", "celebrating", None, "tổ chức, kỷ niệm", "They celebrated their anniversary.", "commemorate, observe", "ignore, overlook"),
    ("celebration", "noun", None, None, None, None, "lễ kỷ niệm, sự ăn mừng", "The celebration lasted all night.", "party, festivity", "mourning, lamentation"),
    ("celebrity", "noun", None, None, None, None, "người nổi tiếng", "She is a famous celebrity.", "star, icon", "unknown, nobody"),
    ("cell", "noun", None, None, None, None, "tế bào, phòng giam", "The prisoner was in a cell.", "chamber, compartment", "open space, freedom"),
    ("center", "noun", None, None, None, None, "trung tâm, giữa", "The city center is crowded.", "middle, heart", "periphery, edge"),
    ("central", "adj", None, None, None, None, "trung tâm, chính", "The central office is in Hanoi.", "main, primary", "secondary, peripheral"),
    ("century", "noun", None, None, None, None, "thế kỷ", "The 21st century is exciting.", "hundred years, era", "moment, instant"),
    ("CEO", "noun", None, None, None, None, "giám đốc điều hành", "He is the CEO of the company.", "chief executive, director", "employee, worker"),
    ("ceremony", "noun", None, None, None, None, "lễ, nghi lễ", "The wedding ceremony was beautiful.", "ritual, observance", "casual, informal"),
    ("certain", "adj", None, None, None, None, "chắc chắn, nhất định", "I am certain about my answer.", "sure, confident", "uncertain, doubtful"),
    ("certainly", "adv", None, None, None, None, "chắc chắn, dĩ nhiên", "I will certainly help you.", "definitely, surely", "probably, maybe"),
    ("chain", "noun", None, None, None, None, "dây xích, chuỗi", "She wore a gold chain.", "link, shackle", "break, sever"),
    ("chair", "noun", None, None, None, None, "ghế", "He sat on the chair.", "seat, stool", "table, desk"),
    ("chairman", "noun", None, None, None, None, "chủ tịch, trưởng ban", "He is the chairman of the board.", "president, leader", "member, follower"),
    ("challenge", "noun", None, None, None, None, "thử thách, sự thách thức", "The job is a big challenge.", "difficulty, obstacle", "ease, simplicity"),
    ("chamber", "noun", None, None, None, None, "phòng, buồng", "The chamber was dark.", "room, space", "hallway, corridor"),
    ("champion", "noun", None, None, None, None, "nhà vô địch", "She is the tennis champion.", "titleholder, winner", "loser, defeated"),
    ("championship", "noun", None, None, None, None, "giải vô địch", "He won the championship.", "tournament, contest", "elimination, defeat"),
    ("chance", "noun", None, None, None, None, "cơ hội, sự may rủi", "You have a good chance to win.", "opportunity, prospect", "risk, danger"),
    ("change", "verb", "changed", "changed", "changing", None, "thay đổi, đổi", "She changed her mind.", "alter, modify", "maintain, preserve"),
    ("changing", "adj", None, None, None, None, "đang thay đổi", "The weather is changing.", "evolving, shifting", "static, constant"),
    ("channel", "noun", None, None, None, None, "kênh, rãnh", "Change the TV channel.", "frequency, station", "silence, stillness"),
    ("chapter", "noun", None, None, None, None, "chương, phần", "Read the next chapter.", "section, part", "whole, entirety"),
    ("character", "noun", None, None, None, None, "nhân vật, tính cách", "He is a main character in the story.", "protagonist, figure", "antagonist, enemy"),
    ("characteristic", "noun", None, None, None, None, "đặc điểm, tính chất", "Honesty is a good characteristic.", "trait, feature", "flaw, defect"),
    ("characterize", "verb", "characterized", "characterized", "characterizing", None, "mô tả đặc điểm, đặc trưng", "The book is characterized by humor.", "depict, represent", "misrepresent, distort"),
    ("charge", "verb", "charged", "charged", "charging", None, "tính phí, sạc điện", "He charged his phone.", "load, power", "drain, exhaust"),
    ("charity", "noun", None, None, None, None, "từ thiện, lòng nhân ái", "She donated to charity.", "philanthropy, benevolence", "selfishness, greed"),
    ("chart", "noun", None, None, None, None, "biểu đồ, bảng", "The chart shows the results.", "graph, diagram", "text, narrative"),
    ("chase", "verb", "chased", "chased", "chasing", None, "đuổi theo, săn bắt", "The dog chased the cat.", "pursue, follow", "escape, flee"),
    ("cheap", "adj", None, None, None, None, "rẻ, không đắt", "The shoes are cheap.", "inexpensive, low-cost", "expensive, costly"),
    ("check", "verb", "checked", "checked", "checking", None, "kiểm tra, kiểm soát", "Check your answers.", "verify, inspect", "ignore, overlook"),
    ("cheek", "noun", None, None, None, None, "má, gò má", "She kissed him on the cheek.", "face, jaw", "forehead, chin"),
    ("cheese", "noun", None, None, None, None, "phô mai", "I like cheese on my pizza.", "dairy, cheddar", "non-dairy, vegan"),
    ("chef", "noun", None, None, None, None, "đầu bếp", "He is a famous chef.", "cook, culinary artist", "amateur, novice"),
    ("chemical", "adj", None, None, None, None, "hóa học, chất hóa học", "Chemical reactions are important.", "elemental, molecular", "physical, mechanical"),
    ("chest", "noun", None, None, None, None, "ngực, rương", "He has pain in his chest.", "thorax, breast", "abdomen, back"),
    ("chicken", "noun", None, None, None, None, "gà, thịt gà", "We had chicken for dinner.", "poultry, fowl", "beef, pork"),
    ("chief", "noun", None, None, None, None, "lãnh đạo, thủ lĩnh", "He is the chief of police.", "leader, head", "subordinate, follower"),
    ("child", "noun", None, None, None, None, "trẻ em, đứa trẻ", "The child is playing.", "kid, youth", "adult, elder"),
    ("childhood", "noun", None, None, None, None, "tuổi thơ", "She remembers her childhood.", "youth, adolescence", "adulthood, maturity"),
    ("Chinese", "adj", None, None, None, None, "người Trung Quốc, thuộc về Trung Quốc", "He is Chinese.", "from China, Sino-", "non-Chinese, foreign"),
    ("chip", "noun", None, None, None, None, "khoai tây chiên, vi mạch", "He ate a potato chip.", "snack, crisp", "meal, whole food"),
    ("chocolate", "noun", None, None, None, None, "sô cô la", "She loves chocolate.", "cocoa, sweet", "bitter, unsweetened"),
    ("choice", "noun", None, None, None, None, "sự lựa chọn", "You have a choice.", "option, selection", "rejection, refusal"),
    ("cholesterol", "noun", None, None, None, None, "cholesterol, mỡ trong máu", "High cholesterol is unhealthy.", "lipid, fat", "protein, carbohydrate"),
    ("choose", "verb", "chose", "chosen", "choosing", None, "chọn, lựa chọn", "She chose the red dress.", "select, pick", "reject, dismiss"),
    ("Christian", "adj", None, None, None, None, "người theo đạo Thiên Chúa, thuộc về Thiên Chúa giáo", "He is Christian.", "believer, follower", "non-Christian, atheist"),
    ("Christmas", "noun", None, None, None, None, "Giáng sinh", "Christmas is in December.", "holiday, festivity", "workday, weekday"),
    ("church", "noun", None, None, None, None, "nhà thờ", "They go to church every Sunday.", "place of worship, chapel", "secular, non-religious"),
    ("cigarette", "noun", None, None, None, None, "thuốc lá", "He smokes a cigarette.", "cigar, smoke", "pipe, vapor"),
    ("circle", "noun", None, None, None, None, "hình tròn, vòng tròn", "Draw a circle on the paper.", "ring, round", "square, rectangle"),
    ("circumstance", "noun", None, None, None, None, "hoàn cảnh, tình huống", "Under these circumstances, we must act.", "situation, condition", "irrelevance, insignificance"),
    ("cite", "verb", "cited", "cited", "citing", None, "trích dẫn, nêu ra", "She cited a famous author.", "quote, mention", "ignore, overlook"),
    ("citizen", "noun", None, None, None, None, "công dân", "He is a Vietnamese citizen.", "national, resident", "foreigner, non-citizen"),
    ("city", "noun", None, None, None, None, "thành phố", "Hanoi is a big city.", "metropolis, urban area", "village, countryside"),
    ("civil", "adj", None, None, None, None, "dân sự, thuộc về dân", "Civil rights are important.", "public, societal", "military, armed"),
    ("civilian", "noun", None, None, None, None, "thường dân", "The civilians were evacuated.", "non-combatant, citizen", "soldier, combatant"),
    ("claim", "verb", "claimed", "claimed", "claiming", None, "yêu cầu, khẳng định", "She claimed the prize.", "assert, maintain", "relinquish, deny"),
    ("class", "noun", None, None, None, None, "lớp học, loại", "The class starts at 8 AM.", "group, category", "individual, singleton"),
    ("classic", "adj", None, None, None, None, "kinh điển, cổ điển", "This is a classic novel.", "timeless, traditional", "modern, novel"),
    ("classroom", "noun", None, None, None, None, "phòng học", "The classroom is clean.", "learning space, lecture hall", "office, hallway"),
    ("clean", "adj", None, None, None, None, "sạch sẽ", "The kitchen is clean.", "tidy, spotless", "dirty, messy"),
    ("clear", "adj", None, None, None, None, "rõ ràng, trong suốt", "The sky is clear today.", "obvious, evident", "cloudy, vague"),
    ("clearly", "adv", None, None, None, None, "một cách rõ ràng", "She spoke clearly.", "distinctly, plainly", "unclearly, vaguely"),
    ("client", "noun", None, None, None, None, "khách hàng", "The client is satisfied.", "customer, consumer", "provider, supplier"),
    ("climb", "verb", "climbed", "climbed", "climbing", None, "leo, trèo", "He climbed the mountain.", "ascend, scale", "descend, lower"),
    ("clinic", "noun", None, None, None, None, "phòng khám", "She works at a clinic.", "medical facility, infirmary", "hospital, home"),
    ("clinical", "adj", None, None, None, None, "lâm sàng, thuộc về lâm sàng", "Clinical trials are necessary.", "experimental, research", "practical, applied"),
    ("clock", "noun", None, None, None, None, "đồng hồ", "The clock shows 3 PM.", "timepiece, watch", "calendar, schedule"),
    ("close", "verb", "closed", "closed", "closing", None, "đóng, gần", "She closed the door.", "shut, seal", "open, unlock"),
    ("closely", "adv", None, None, None, None, "một cách gần gũi, sát sao", "They work closely together.", "intimately, directly", "remotely, loosely"),
    ("closer", "adj", None, None, None, None, "gần hơn, sát hơn", "Move closer to the board.", "nearer, tighter", "farther, looser"),
    ("clothes", "noun", None, None, None, None, "quần áo", "She bought new clothes.", "apparel, garments", "nakedness, undress"),
    ("clothing", "noun", None, None, None, None, "quần áo, trang phục", "Winter clothing is warm.", "attire, garments", "nudity, undress"),
    ("cloud", "noun", None, None, None, None, "đám mây", "The cloud is white.", "vapor, mist", "clear sky, sunshine"),
    ("club", "noun", None, None, None, None, "câu lạc bộ, gậy", "He joined the tennis club.", "association, organization", "lone wolf, individual"),
    ("clue", "noun", None, None, None, None, "manh mối, đầu mối", "The detective found a clue.", "hint, indication", "blindness, ignorance"),
    ("cluster", "noun", None, None, None, None, "nhóm, cụm", "A cluster of stars was visible.", "group, bunch", "individual, singleton"),
    ("coach", "noun", None, None, None, None, "huấn luyện viên, xe khách", "He is a football coach.", "trainer, instructor", "player, amateur"),
    ("coal", "noun", None, None, None, None, "than đá", "Coal is used for fuel.", "carbon, fossil fuel", "renewable, clean energy"),
    ("coalition", "noun", None, None, None, None, "liên minh, liên kết", "The coalition formed a government.", "alliance, partnership", "division, disunity"),
    ("coast", "noun", None, None, None, None, "bờ biển", "They walked along the coast.", "shoreline, beach", "inland, center"),
    ("coat", "noun", None, None, None, None, "áo khoác, lớp phủ", "She wore a warm coat.", "jacket, overcoat", "naked, uncovered"),
    ("code", "noun", None, None, None, None, "mã, quy tắc", "Enter the code to unlock.", "cipher, key", "randomness, chaos"),
    ("coffee", "noun", None, None, None, None, "cà phê", "He drinks coffee every morning.", "brew, java", "decaf, tea"),
    ("cognitive", "adj", None, None, None, None, "nhận thức, thuộc về nhận thức", "Cognitive skills are important.", "mental, intellectual", "physical, manual"),
    ("cold", "adj", None, None, None, None, "lạnh, cảm lạnh", "The weather is cold.", "chilly, cool", "warm, hot"),
    ("collapse", "verb", "collapsed", "collapsed", "collapsing", None, "sụp đổ, ngã xuống", "The building collapsed.", "fall, cave in", "rise, ascend"),
    ("colleague", "noun", None, None, None, None, "đồng nghiệp", "She is my colleague.", "co-worker, associate", "manager, supervisor"),
    ("collect", "verb", "collected", "collected", "collecting", None, "thu thập, sưu tầm", "He collects stamps.", "gather, assemble", "disperse, scatter"),
    ("collection", "noun", None, None, None, None, "bộ sưu tập, sự thu thập", "Her collection of books is large.", "assortment, compilation", "dispersal, scattering"),
    ("collective", "adj", None, None, None, None, "tập thể, chung", "It was a collective effort.", "joint, shared", "individual, solo"),
    ("college", "noun", None, None, None, None, "trường cao đẳng, đại học", "She goes to college.", "university, institution", "high school, primary school"),
    ("colonial", "adj", None, None, None, None, "thuộc địa, thực dân", "Colonial history is interesting.", "settler, imperial", "native, indigenous"),
    ("color", "noun", None, None, None, None, "màu sắc", "Red is my favorite color.", "hue, shade", "colorlessness, whiteness"),
    ("column", "noun", None, None, None, None, "cột, mục", "The column is tall.", "pillar, post", "beam, slab"),
    ("dad", "noun", None, None, None, None, "bố, cha", "My dad is very kind.", "father, papa", "mother, sister"),
    ("daily", "adj", None, None, None, None, "hàng ngày", "She reads the newspaper daily.", "everyday, routine", "occasionally, seldom"),
    ("damage", "noun", None, None, None, None, "thiệt hại, hư hỏng", "The storm caused damage.", "harm, injury", "repair, restoration"),
    ("dance", "verb", "danced", "danced", "dancing", None, "nhảy, khiêu vũ", "They danced all night.", "boogie, sway", "sit, remain"),
    ("danger", "noun", None, None, None, None, "nguy hiểm", "There is danger ahead.", "risk, hazard", "safety, security"),
    ("dangerous", "adj", None, None, None, None, "nguy hiểm", "The road is dangerous.", "risky, hazardous", "safe, secure"),
    ("dare", "verb", "dared", "dared", "daring", None, "dám, thách thức", "He dared to speak out.", "challenge, defy", "fear, withdraw"),
    ("dark", "adj", None, None, None, None, "tối, đen tối", "The room is dark.", "dim, shadowy", "bright, illuminated"),
    ("darkness", "noun", None, None, None, None, "bóng tối, sự tối", "Darkness fell quickly.", "night, gloom", "light, brightness"),
    ("data", "noun", None, None, None, None, "dữ liệu", "The data is accurate.", "information, details", "misinformation, errors"),
    ("date", "noun", None, None, None, None, "ngày, cuộc hẹn", "What is today's date?", "day, appointment", "past, history"),
    ("daughter", "noun", None, None, None, None, "con gái", "His daughter is five years old.", "girl, offspring", "son, child"),
    ("day", "noun", None, None, None, None, "ngày", "Today is a sunny day.", "24-hour period, daytime", "night, evening"),
    ("dead", "adj", None, None, None, None, "chết, đã chết", "The battery is dead.", "deceased, lifeless", "alive, living"),
    ("deal", "noun", None, None, None, None, "thỏa thuận, giao dịch", "They made a deal.", "agreement, arrangement", "disagreement, dispute"),
    ("dealer", "noun", None, None, None, None, "người buôn bán, đại lý", "He is a car dealer.", "merchant, trader", "buyer, customer"),
    ("dear", "adj", None, None, None, None, "thân yêu, quý giá", "She is my dear friend.", "beloved, cherished", "hated, despised"),
    ("death", "noun", None, None, None, None, "cái chết", "He was sad after the death of his pet.", "demise, passing", "birth, beginning"),
    ("debate", "noun", None, None, None, None, "cuộc tranh luận, tranh cãi", "The debate lasted two hours.", "discussion, argument", "agreement, harmony"),
    ("debt", "noun", None, None, None, None, "nợ, khoản nợ", "He paid off his debt.", "obligation, liability", "credit, asset"),
    ("decade", "noun", None, None, None, None, "thập kỷ, mười năm", "A decade has passed.", "ten years, period", "moment, instant"),
    ("decide", "verb", "decided", "decided", "deciding", None, "quyết định", "She decided to go abroad.", "determine, conclude", "hesitate, waver"),
    ("decision", "noun", None, None, None, None, "quyết định", "His decision was final.", "choice, conclusion", "indecision, hesitation"),
    ("deck", "noun", None, None, None, None, "boong tàu, sàn nhà", "They sat on the deck.", "platform, floor", "cabin, room"),
    ("declare", "verb", "declared", "declared", "declaring", None, "tuyên bố, công bố", "He declared his innocence.", "proclaim, announce", "conceal, hide"),
    ("decline", "verb", "declined", "declined", "declining", None, "giảm, từ chối", "Sales declined last year.", "decrease, diminish", "increase, rise"),
    ("decrease", "verb", "decreased", "decreased", "decreasing", None, "giảm, hạ xuống", "The price decreased.", "reduce, lessen", "increase, raise"),
    ("deep", "adj", None, None, None, None, "sâu, sâu sắc", "The water is deep.", "profound, intense", "shallow, superficial"),
    ("deeply", "adv", None, None, None, None, "sâu sắc, hết sức", "She is deeply grateful.", "profoundly, intensely", "superficially, lightly"),
    ("deer", "noun", None, None, None, None, "con hươu, nai", "A deer ran across the road.", "doe, stag", "dog, cat"),
    ("defeat", "verb", "defeated", "defeated", "defeating", None, "đánh bại, thất bại", "They defeated the enemy.", "conquer, overcome", "lose, surrender"),
    ("defend", "verb", "defended", "defended", "defending", None, "bảo vệ, phòng thủ", "He defended his opinion.", "protect, guard", "attack, assault"),
    ("defendant", "noun", None, None, None, None, "bị cáo, người bị kiện", "The defendant was found guilty.", "accused, litigant", "plaintiff, complainant"),
    ("defense", "noun", None, None, None, None, "sự phòng thủ, bảo vệ", "The team played good defense.", "protection, safeguarding", "attack, offense"),
    ("defensive", "adj", None, None, None, None, "phòng thủ, bảo vệ", "He took a defensive position.", "protective, shielding", "aggressive, offensive"),
    ("deficit", "noun", None, None, None, None, "thâm hụt, thiếu hụt", "The budget has a deficit.", "shortfall, deficiency", "surplus, excess"),
    ("define", "verb", "defined", "defined", "defining", None, "định nghĩa, xác định", "She defined the term.", "explain, clarify", "confuse, obscure"),
    ("definitely", "adv", None, None, None, None, "chắc chắn, dứt khoát", "I will definitely come.", "certainly, surely", "probably, maybe"),
    ("definition", "noun", None, None, None, None, "định nghĩa", "The definition is clear.", "explanation, meaning", "ambiguity, confusion"),
    ("degree", "noun", None, None, None, None, "bằng cấp, độ", "He has a master's degree.", "qualification, diploma", "ignorance, illiteracy"),
    ("delay", "verb", "delayed", "delayed", "delaying", None, "trì hoãn, chậm trễ", "The flight was delayed.", "postpone, defer", "hasten, expedite"),
    ("deliver", "verb", "delivered", "delivered", "delivering", None, "giao hàng, trình bày", "He delivered the package.", "bring, transport", "receive, accept"),
    ("delivery", "noun", None, None, None, None, "sự giao hàng, sự trình bày", "The delivery was late.", "shipment, distribution", "pickup, collection"),
    ("demand", "noun", None, None, None, None, "nhu cầu, yêu cầu", "There is high demand for rice.", "need, requirement", "supply, availability"),
    ("democracy", "noun", None, None, None, None, "dân chủ", "Democracy is important.", "self-government, republic", "autocracy, dictatorship"),
    ("Democrat", "noun", None, None, None, None, "đảng viên Dân chủ", "He is a Democrat.", "liberal, progressive", "Republican, conservative"),
    ("democratic", "adj", None, None, None, None, "dân chủ, thuộc về dân chủ", "The country is democratic.", "representative, electoral", "authoritarian, dictatorial"),
    ("demonstrate", "verb", "demonstrated", "demonstrated", "demonstrating", None, "chứng minh, biểu tình", "She demonstrated the process.", "show, illustrate", "conceal, hide"),
    ("demonstration", "noun", None, None, None, None, "cuộc biểu tình, sự chứng minh", "The demonstration was peaceful.", "protest, rally", "suppression, censorship"),
    ("deny", "verb", "denied", "denied", "denying", None, "phủ nhận, từ chối", "He denied the accusation.", "refuse, reject", "accept, admit"),
    ("department", "noun", None, None, None, None, "phòng ban, bộ phận", "She works in the sales department.", "division, section", "whole, entirety"),
    ("depend", "verb", "depended", "depended", "depending", None, "phụ thuộc, dựa vào", "Children depend on their parents.", "rely on, count on", "independent, self-sufficient"),
    ("dependent", "adj", None, None, None, None, "phụ thuộc, lệ thuộc", "He is dependent on his family.", "reliant, subordinate", "independent, self-sufficient"),
    ("depending", "adv", None, None, None, None, "tùy thuộc vào", "Depending on the weather, we may go.", "contingent on, based on", "regardless, independent of"),
    ("depict", "verb", "depicted", "depicted", "depicting", None, "miêu tả, vẽ", "The painting depicts a landscape.", "illustrate, portray", "conceal, hide"),
    ("depression", "noun", None, None, None, None, "sự trầm cảm, suy thoái", "He suffers from depression.", "melancholy, gloom", "happiness, joy"),
    ("depth", "noun", None, None, None, None, "độ sâu, chiều sâu", "The depth of the lake is unknown.", "deepness, profundity", "shallowness, surface"),
    ("deputy", "noun", None, None, None, None, "phó, người đại diện", "He is the deputy manager.", "assistant, aide", "superior, chief"),
    ("derive", "verb", "derived", "derived", "deriving", None, "lấy được, bắt nguồn từ", "The word derives from Latin.", "originate, stem", "cease, stop"),
    ("describe", "verb", "described", "described", "describing", None, "miêu tả, mô tả", "She described the scene.", "depict, portray", "conceal, hide"),
    ("description", "noun", None, None, None, None, "sự miêu tả, mô tả", "The description is detailed.", "depiction, account", "concealment, suppression"),
    ("desert", "noun", None, None, None, None, "sa mạc", "The desert is hot and dry.", "wasteland, arid region", "oasis, fertile land"),
    ("deserve", "verb", "deserved", "deserved", "deserving", None, "xứng đáng, đáng được", "She deserves a reward.", "merit, earn", "forfeit, lose"),
    ("design", "verb", "designed", "designed", "designing", None, "thiết kế, tạo ra", "He designed the building.", "plan, create", "destroy, ruin"),
    ("designer", "noun", None, None, None, None, "nhà thiết kế", "She is a fashion designer.", "creator, stylist", "consumer, buyer"),
    ("desire", "noun", None, None, None, None, "mong muốn, khao khát", "He has a desire to travel.", "wish, longing", "aversion, disgust"),
    ("desk", "noun", None, None, None, None, "bàn làm việc", "The desk is made of wood.", "table, workstation", "floor, ceiling"),
    ("desperate", "adj", None, None, None, None, "tuyệt vọng, liều lĩnh", "He was desperate for help.", "hopeless, frantic", "optimistic, hopeful"),
    ("despite", "prep", None, None, None, None, "mặc dù, bất chấp", "Despite the rain, we went out.", "in spite of, notwithstanding", "because of, due to"),
    ("destroy", "verb", "destroyed", "destroyed", "destroying", None, "phá hủy, tiêu diệt", "The fire destroyed the house.", "ruin, demolish", "build, create"),
    ("destruction", "noun", None, None, None, None, "sự phá hủy, sự tiêu diệt", "The destruction was complete.", "devastation, annihilation", "construction, creation"),
    ("detail", "noun", None, None, None, None, "chi tiết, tiểu tiết", "The report includes every detail.", "particular, specific", "general, whole"),
    ("detailed", "adj", None, None, None, None, "chi tiết, tỉ mỉ", "She gave a detailed explanation.", "thorough, comprehensive", "vague, general"),
    ("detect", "verb", "detected", "detected", "detecting", None, "phát hiện, dò ra", "The test detected the virus.", "discover, identify", "miss, overlook"),
    ("determine", "verb", "determined", "determined", "determining", None, "xác định, quyết định", "She determined the cause.", "ascertain, establish", "ignore, overlook"),
    ("develop", "verb", "developed", "developed", "developing", None, "phát triển, mở rộng", "The company developed new products.", "expand, grow", "shrink, reduce"),
    ("developing", "adj", None, None, None, None, "đang phát triển", "Vietnam is a developing country.", "emerging, growing", "developed, mature"),
    ("development", "noun", None, None, None, None, "sự phát triển, mở rộng", "The development was rapid.", "progress, advancement", "decline, regression"),
    ("device", "noun", None, None, None, None, "thiết bị, dụng cụ", "He bought a new device.", "gadget, appliance", "manual, tool"),
    ("devote", "verb", "devoted", "devoted", "devoting", None, "cống hiến, dành cho", "She devoted her life to science.", "dedicate, commit", "neglect, ignore"),
    ("dialogue", "noun", None, None, None, None, "đối thoại, cuộc hội thoại", "The dialogue was interesting.", "conversation, discussion", "silence, monologue"),
    ("die", "verb", "died", "died", "dying", None, "chết, qua đời", "The plant died.", "expire, perish", "live, survive"),
    ("diet", "noun", None, None, None, None, "chế độ ăn uống, kiêng ăn", "She follows a healthy diet.", "nutrition, regimen", "fast, feast"),
    ("differ", "verb", "differed", "differed", "differing", None, "khác nhau, bất đồng", "Opinions differ on this issue.", "vary, diverge", "agree, coincide"),
    ("difference", "noun", None, None, None, None, "sự khác biệt, khác nhau", "There is a big difference.", "disparity, distinction", "similarity, resemblance"),
    ("different", "adj", None, None, None, None, "khác nhau, khác biệt", "They have different ideas.", "diverse, distinct", "same, identical"),
    ("differently", "adv", None, None, None, None, "khác nhau, khác biệt", "She thinks differently.", "uniquely, alternatively", "similarly, alike"),
    ("difficult", "adj", None, None, None, None, "khó khăn, khó", "The exam was difficult.", "challenging, tough", "easy, simple"),
    ("difficulty", "noun", None, None, None, None, "sự khó khăn, trở ngại", "He had difficulty breathing.", "trouble, challenge", "ease, simplicity"),
    ("dig", "verb", "dug", "dug", "digging", None, "đào, bới", "He dug a hole.", "excavate, burrow", "fill, close"),
    ("digital", "adj", None, None, None, None, "kỹ thuật số, thuộc về số", "She has a digital camera.", "electronic, computerized", "analog, manual"),
    ("dimension", "noun", None, None, None, None, "kích thước, chiều", "The room has large dimensions.", "size, measurement", "insignificance, triviality"),
    ("dining", "noun", None, None, None, None, "ăn uống, phòng ăn", "The dining room is spacious.", "eating, mealtime", "kitchen, living room"),
    ("dinner", "noun", None, None, None, None, "bữa tối", "We had chicken for dinner.", "evening meal, supper", "breakfast, lunch"),
    ("direct", "verb", "directed", "directed", "directing", None, "chỉ đạo, hướng dẫn", "He directed the movie.", "manage, guide", "mislead, confuse"),
    ("direction", "noun", None, None, None, None, "phương hướng, chỉ dẫn", "She gave directions to the station.", "guidance, instructions", "confusion, disorientation"),
    ("directly", "adv", None, None, None, None, "trực tiếp, thẳng", "He answered directly.", "straightforwardly, honestly", "indirectly, evasively"),
    ("director", "noun", None, None, None, None, "giám đốc, đạo diễn", "She is the director of the company.", "manager, administrator", "employee, worker"),
    ("dirt", "noun", None, None, None, None, "bụi bẩn, đất", "The car is covered in dirt.", "soil, grime", "cleanliness, purity"),
    ("dirty", "adj", None, None, None, None, "bẩn, dơ", "The floor is dirty.", "unclean, filthy", "clean, spotless"),
    ("disability", "noun", None, None, None, None, "khuyết tật, sự bất lực", "He lives with a disability.", "impairment, handicap", "ability, capability"),
    ("disagree", "verb", "disagreed", "disagreed", "disagreeing", None, "không đồng ý, bất đồng", "They disagreed on the plan.", "differ, oppose", "agree, concur"),
    ("disappear", "verb", "disappeared", "disappeared", "disappearing", None, "biến mất, biến đi", "The cat disappeared suddenly.", "vanish, fade away", "appear, emerge"),
    ("disaster", "noun", None, None, None, None, "thảm họa, tai họa", "The flood was a disaster.", "catastrophe, calamity", "blessing, miracle"),
    ("discipline", "noun", None, None, None, None, "kỷ luật, ngành học", "He has good discipline.", "self-control, training", "chaos, disorder"),
    ("discourse", "noun", None, None, None, None, "bài diễn thuyết, đàm thoại", "The discourse was interesting.", "discussion, dialogue", "silence, non-communication"),
    ("discover", "verb", "discovered", "discovered", "discovering", None, "khám phá, phát hiện", "She discovered a new species.", "find, uncover", "lose, overlook"),
    ("discovery", "noun", None, None, None, None, "sự khám phá, phát hiện", "The discovery was important.", "finding, revelation", "ignorance, oblivion"),
    ("discrimination", "noun", None, None, None, None, "sự phân biệt đối xử", "They fight against discrimination.", "prejudice, bias", "fairness, equality"),
    ("discuss", "verb", "discussed", "discussed", "discussing", None, "thảo luận, bàn bạc", "They discussed the project.", "talk about, debate", "ignore, overlook"),
    ("discussion", "noun", None, None, None, None, "cuộc thảo luận, bàn bạc", "The discussion was helpful.", "debate, dialogue", "silence, non-communication"),
    ("disease", "noun", None, None, None, None, "bệnh, dịch bệnh", "He suffers from a rare disease.", "illness, disorder", "health, wellness"),
    ("dish", "noun", None, None, None, None, "món ăn, đĩa", "The dish is delicious.", "plate, cuisine", "ingredient, component"),
    ("dismiss", "verb", "dismissed", "dismissed", "dismissing", None, "sa thải, bác bỏ", "He was dismissed from his job.", "fire, terminate", "hire, employ"),
    ("disorder", "noun", None, None, None, None, "rối loạn, lộn xộn", "He has a sleep disorder.", "disturbance, disruption", "order, organization"),
    ("display", "verb", "displayed", "displayed", "displaying", None, "trưng bày, hiển thị", "The store displayed new products.", "exhibit, showcase", "conceal, hide"),
    ("dispute", "noun", None, None, None, None, "tranh chấp, bất đồng", "The dispute lasted for months.", "disagreement, argument", "agreement, harmony"),
    ("distance", "noun", None, None, None, None, "khoảng cách, xa cách", "The distance is 10 kilometers.", "space, interval", "closeness, proximity"),
    ("distant", "adj", None, None, None, None, "xa, xa cách", "The island is distant.", "faraway, remote", "near, close"),
    ("distinct", "adj", None, None, None, None, "riêng biệt, rõ ràng", "There are two distinct groups.", "different, separate", "similar, alike"),
    ("distinction", "noun", None, None, None, None, "sự khác biệt, sự phân biệt", "She graduated with distinction.", "difference, contrast", "similarity, resemblance"),
    ("distinguish", "verb", "distinguished", "distinguished", "distinguishing", None, "phân biệt, nhận ra", "He distinguished the twins.", None, None),
    ("distribute", "verb", "distributed", "distributed", "distributing", None, "phân phát, phân phối", "They distributed food to the poor.", None, None),
    ("distribution", "noun", None, None, None, None, "sự phân phối, sự phân phát", "The distribution was fair.", None, None),
    ("district", "noun", None, None, None, None, "quận, huyện, khu vực", "She lives in the central district.", None, None),
    ("diverse", "adj", None, None, None, None, "đa dạng, khác nhau", "The city is diverse.", None, None),
    ("diversity", "noun", None, None, None, None, "sự đa dạng, khác biệt", "Cultural diversity is important.", None, None),
    ("divide", "verb", "divided", "divided", "dividing", None, "chia, phân chia", "They divided the cake.", None, None),
    ("division", "noun", None, None, None, None, "sự phân chia, bộ phận", "The division is responsible for sales.", None, None),
    ("divorce", "noun", None, None, None, None, "ly hôn, sự ly dị", "They got a divorce.", None, None),
    ("DNA", "noun", None, None, None, None, "DNA, gen di truyền", "DNA testing is accurate.", None, None),
    ("do", "verb", "did", "done", "doing", None, "làm, thực hiện", "She does her homework.", None, None),
    ("doctor", "noun", None, None, None, None, "bác sĩ, tiến sĩ", "He is a doctor.", None, None),
    ("document", "noun", None, None, None, None, "tài liệu, văn bản", "She signed the document.", None, None),
    ("dog", "noun", None, None, None, None, "con chó", "The dog is barking.", None, None),
    ("domestic", "adj", None, None, None, None, "trong nước, nội địa", "Domestic flights are cheaper.", None, None),
    ("dominant", "adj", None, None, None, None, "chiếm ưu thế, vượt trội", "He is the dominant player.", None, None),
    ("dominate", "verb", "dominated", "dominated", "dominating", None, "thống trị, chi phối", "She dominates the market.", None, None),
    ("door", "noun", None, None, None, None, "cửa ra vào", "He opened the door.", None, None),
    ("double", "adj", None, None, None, None, "gấp đôi, đôi", "She ordered a double portion.", None, None),
    ("doubt", "noun", None, None, None, None, "nghi ngờ, sự nghi ngờ", "He has doubt about the result.", None, None),
    ("down", "adv", None, None, None, None, "xuống, phía dưới", "She went down the stairs.", None, None),
    ("downtown", "noun", None, None, None, None, "trung tâm thành phố", "He works downtown.", None, None),
    ("dozen", "noun", None, None, None, None, "tá, một tá", "She bought a dozen eggs.", None, None),
    ("draft", "noun", None, None, None, None, "bản nháp, dự thảo", "He wrote a draft of the letter.", None, None),
    ("drag", "verb", "dragged", "dragged", "dragging", None, "kéo, lôi", "He dragged the box.", None, None),
    ("drama", "noun", None, None, None, None, "kịch, phim truyền hình", "She likes drama movies.", None, None),
    ("dramatic", "adj", None, None, None, None, "kịch tính, ấn tượng", "The ending was dramatic.", None, None),
    ("dramatically", "adv", None, None, None, None, "một cách kịch tính, đột ngột", "Sales increased dramatically.", None, None),
    ("draw", "verb", "drew", "drawn", "drawing", None, "vẽ, kéo", "She drew a picture.", None, None),
    ("drawing", "noun", None, None, None, None, "bức vẽ, sự vẽ", "Her drawing is beautiful.", None, None),
    ("dream", "noun", None, None, None, None, "giấc mơ, mơ ước", "He had a strange dream.", None, None),
    ("dress", "noun", None, None, None, None, "váy, áo đầm", "She wore a red dress.", None, None),
    ("drink", "verb", "drank", "drunk", "drinking", None, "uống, đồ uống", "He drank water.", None, None),
    ("drive", "verb", "drove", "driven", "driving", None, "lái xe, điều khiển", "She drives to work.", None, None),
    ("driver", "noun", None, None, None, None, "tài xế, người lái xe", "He is a taxi driver.", None, None),
    ("drop", "verb", "dropped", "dropped", "dropping", None, "rơi, thả", "She dropped her keys.", None, None),
    ("drug", "noun", None, None, None, None, "thuốc, ma túy", "He takes medicine and drugs.", None, None),
    ("dry", "adj", None, None, None, None, "khô, làm khô", "The clothes are dry.", None, None),
    ("due", "adj", None, None, None, None, "đến hạn, do bởi", "The payment is due tomorrow.", None, None),
    ("during", "prep", None, None, None, None, "trong lúc, trong khi", "She slept during the movie.", None, None),
    ("dust", "noun", None, None, None, None, "bụi, bụi bẩn", "The table is covered in dust.", None, None),
    ("duty", "noun", None, None, None, None, "nhiệm vụ, trách nhiệm", "It is his duty to help.", None, None),
    ("each", "pron", None, None, None, None, "mỗi, từng", "Each student has a book.", None, None),
    ("eager", "adj", None, None, None, None, "háo hức, nhiệt tình", "She is eager to learn.", None, None),
    ("ear", "noun", None, None, None, None, "tai, lỗ tai", "He has a pain in his ear.", None, None),
    ("early", "adj", None, None, None, None, "sớm, ban đầu", "She gets up early.", None, None),
    ("earn", "verb", "earned", "earned", "earning", None, "kiếm được, đạt được", "He earned a lot of money.", None, None),
    ("earnings", "noun", None, None, None, None, "thu nhập, tiền lương", "Her earnings are high.", None, None),
    ("earth", "noun", None, None, None, None, "trái đất, đất", "The earth is round.", None, None),
    ("ease", "noun", None, None, None, None, "sự dễ dàng, thoải mái", "She completed the task with ease.", None, None),
    ("easily", "adv", None, None, None, None, "dễ dàng, một cách dễ dàng", "He solved the problem easily.", None, None),
    ("east", "noun", None, None, None, None, "phía đông, miền đông", "The sun rises in the east.", None, None),
    ("eastern", "adj", None, None, None, None, "phía đông, thuộc miền đông", "The eastern region is beautiful.", None, None),
    ("easy", "adj", None, None, None, None, "dễ dàng, đơn giản", "The test was easy.", None, None),
    ("eat", "verb", "ate", "eaten", "eating", None, "ăn, dùng bữa", "She eats breakfast at 7.", None, None),
    ("economic", "adj", None, None, None, None, "kinh tế, thuộc về kinh tế", "Economic growth is important.", None, None),
    ("economics", "noun", None, None, None, None, "kinh tế học", "She studies economics.", None, None),
    ("economist", "noun", None, None, None, None, "nhà kinh tế học", "He is an economist.", None, None),
    ("economy", "noun", None, None, None, None, "nền kinh tế", "The economy is growing.", None, None),
    ("edge", "noun", None, None, None, None, "cạnh, bờ, mép", "He stood at the edge of the cliff.", None, None),
    ("edition", "noun", None, None, None, None, "phiên bản, ấn bản", "This is the latest edition.", None, None),
    ("editor", "noun", None, None, None, None, "biên tập viên", "She is the editor of the magazine.", None, None),
    ("educate", "verb", "educated", "educated", "educating", None, "giáo dục, dạy dỗ", "They educate children well.", None, None),
    ("education", "noun", None, None, None, None, "giáo dục, sự học", "Education is important.", None, None),
    ("educational", "adj", None, None, None, None, "thuộc về giáo dục", "This is an educational program.", None, None),
    ("educator", "noun", None, None, None, None, "nhà giáo dục, giáo viên", "He is a respected educator.", None, None),
    ("effect", "noun", None, None, None, None, "hiệu quả, tác động", "The medicine had a good effect.", None, None),
    ("effective", "adj", None, None, None, None, "hiệu quả, có tác dụng", "The new method is effective.", None, None),
    ("effectively", "adv", None, None, None, None, "một cách hiệu quả", "She works effectively.", None, None),
    ("efficiency", "noun", None, None, None, None, "hiệu suất, sự hiệu quả", "Efficiency is important in business.", None, None),
    ("efficient", "adj", None, None, None, None, "hiệu quả, năng suất", "He is an efficient worker.", None, None),
    ("effort", "noun", None, None, None, None, "nỗ lực, cố gắng", "She made a great effort.", None, None),
    ("egg", "noun", None, None, None, None, "trứng", "She ate a boiled egg.", None, None),
    ("eight", "num", None, None, None, None, "tám", "There are eight apples.", None, None),
    ("either", "conj", None, None, None, None, "hoặc, một trong hai", "You can choose either option.", None, None),
    ("elderly", "adj", None, None, None, None, "cao tuổi, già", "The elderly need care.", None, None),
    ("elect", "verb", "elected", "elected", "electing", None, "bầu chọn, lựa chọn", "They elected a new president.", None, None),
    ("election", "noun", None, None, None, None, "cuộc bầu cử", "The election is next month.", None, None),
    ("electric", "adj", None, None, None, None, "điện, chạy bằng điện", "He bought an electric car.", None, None),
    ("electricity", "noun", None, None, None, None, "điện, năng lượng điện", "Electricity is expensive.", None, None),
    ("electronic", "adj", None, None, None, None, "điện tử, thuộc về điện tử", "He sells electronic devices.", None, None),
    ("element", "noun", None, None, None, None, "yếu tố, nguyên tố", "Oxygen is an element.", None, None),
    ("elementary", "adj", None, None, None, None, "cơ bản, tiểu học", "She teaches at an elementary school.", None, None),
    ("eliminate", "verb", "eliminated", "eliminated", "eliminating", None, "loại bỏ, loại trừ", "They eliminated the error.", None, None),
    ("elite", "noun", None, None, None, None, "ưu tú, tinh hoa", "He belongs to the elite.", None, None),
    ("else", "adv", None, None, None, None, "khác, nữa", "Do you want anything else?", None, None),
    ("elsewhere", "adv", None, None, None, None, "nơi khác, chỗ khác", "She looked elsewhere for a job.", None, None),
    ("e-mail", "noun", None, None, None, None, "thư điện tử, email", "He sent an e-mail.", None, None),
    ("embrace", "verb", "embraced", "embraced", "embracing", None, "ôm, đón nhận", "She embraced her friend.", None, None),
    ("emerge", "verb", "emerged", "emerged", "emerging", None, "xuất hiện, nổi lên", "A new leader emerged.", None, None),
    ("emergency", "noun", None, None, None, None, "tình trạng khẩn cấp", "Call 115 in an emergency.", None, None),
    ("emission", "noun", None, None, None, None, "sự phát ra, khí thải", "Car emission is a problem.", None, None),
    ("emotion", "noun", None, None, None, None, "cảm xúc, tình cảm", "She showed no emotion.", None, None),
    ("emotional", "adj", None, None, None, None, "cảm động, thuộc về cảm xúc", "He is an emotional person.", None, None),
    ("emphasis", "noun", None, None, None, None, "sự nhấn mạnh, tầm quan trọng", "She put emphasis on safety.", None, None),
    ("emphasize", "verb", "emphasized", "emphasized", "emphasizing", None, "nhấn mạnh, làm nổi bật", "He emphasized the need for change.", None, None),
    ("employ", "verb", "employed", "employed", "employing", None, "thuê, sử dụng", "The company employs 100 people.", None, None),
    ("employee", "noun", None, None, None, None, "nhân viên, người làm công", "She is a new employee.", None, None),
    ("employer", "noun", None, None, None, None, "chủ, người sử dụng lao động", "He is a good employer.", None, None),
    ("employment", "noun", None, None, None, None, "việc làm, sự tuyển dụng", "She is looking for employment.", None, None),
    ("empty", "adj", None, None, None, None, "trống rỗng, không có gì", "The box is empty.", None, None),
    ("enable", "verb", "enabled", "enabled", "enabling", None, "cho phép, làm cho có thể", "The app enables easy booking.", None, None),
    ("encounter", "verb", "encountered", "encountered", "encountering", None, "gặp phải, chạm trán", "She encountered a problem.", None, None),
    ("encourage", "verb", "encouraged", "encouraged", "encouraging", None, "khuyến khích, động viên", "Her parents encouraged her.", None, None),
    ("end", "noun", None, None, None, None, "kết thúc, cuối cùng", "The end of the story is sad.", None, None),
    ("enemy", "noun", None, None, None, None, "kẻ thù, đối thủ", "He faced his enemy.", None, None),
    ("energy", "noun", None, None, None, None, "năng lượng, sức lực", "She has a lot of energy.", None, None),
    ("enforcement", "noun", None, None, None, None, "sự thực thi, thi hành", "Law enforcement is strict.", None, None),
    ("engage", "verb", "engaged", "engaged", "engaging", None, "tham gia, thu hút", "He engaged in the discussion.", None, None),
    ("engine", "noun", None, None, None, None, "động cơ, máy", "The car engine is powerful.", None, None),
    ("engineer", "noun", None, None, None, None, "kỹ sư, người thiết kế", "He is a software engineer.", None, None),
    ("engineering", "noun", None, None, None, None, "ngành kỹ thuật, công trình", "She studies engineering.", None, None),
    ("English", "noun", None, None, None, None, "tiếng Anh, người Anh", "She speaks English well.", None, None),
    ("enhance", "verb", "enhanced", "enhanced", "enhancing", None, "nâng cao, tăng cường", "The program enhances skills.", None, None),
    ("enjoy", "verb", "enjoyed", "enjoyed", "enjoying", None, "thưởng thức, thích", "She enjoys reading.", None, None),
    ("enormous", "adj", None, None, None, None, "to lớn, khổng lồ", "The building is enormous.", None, None),
    ("enough", "adj", None, None, None, None, "đủ, đầy đủ", "She has enough money.", None, None),
    ("ensure", "verb", "ensured", "ensured", "ensuring", None, "đảm bảo, chắc chắn", "He ensured the safety.", None, None),
    ("enter", "verb", "entered", "entered", "entering", None, "đi vào, nhập vào", "She entered the room.", None, None),
    ("enterprise", "noun", None, None, None, None, "doanh nghiệp, công ty", "He owns an enterprise.", None, None),
    ("entertainment", "noun", None, None, None, None, "giải trí, ngành giải trí", "TV is a form of entertainment.", None, None),
    ("entire", "adj", None, None, None, None, "toàn bộ, toàn thể", "She ate the entire cake.", None, None),
    ("entirely", "adv", None, None, None, None, "hoàn toàn, toàn bộ", "The plan is entirely new.", None, None),
    ("entrance", "noun", None, None, None, None, "lối vào, sự gia nhập", "The entrance is on the left.", None, None),
    ("entry", "noun", None, None, None, None, "sự vào, mục nhập", "Her entry was late.", None, None),
    ("environment", "noun", None, None, None, None, "môi trường, hoàn cảnh", "Protect the environment.", None, None),
    ("environmental", "adj", None, None, None, None, "thuộc về môi trường", "Environmental issues are serious.", None, None),
    ("episode", "noun", None, None, None, None, "tập phim, phần", "I watched the latest episode.", None, None),
    ("equal", "adj", None, None, None, None, "bằng nhau, công bằng", "All people are equal.", None, None),
    ("equally", "adv", None, None, None, None, "một cách công bằng, như nhau", "They shared the prize equally.", None, None),
    ("equipment", "noun", None, None, None, None, "thiết bị, dụng cụ", "The equipment is expensive.", None, None),
    ("era", "noun", None, None, None, None, "thời đại, kỷ nguyên", "We live in a new era.", None, None),
    ("error", "noun", None, None, None, None, "lỗi, sai sót", "There was an error in the report.", None, None),
    ("escape", "verb", "escaped", "escaped", "escaping", None, "trốn thoát, thoát khỏi", "He escaped from prison.", None, None),
    ("especially", "adv", None, None, None, None, "đặc biệt, nhất là", "She likes fruit, especially apples.", None, None),
    ("essay", "noun", None, None, None, None, "bài luận, bài viết", "She wrote an essay.", None, None),
    ("essential", "adj", None, None, None, None, "cần thiết, thiết yếu", "Water is essential for life.", None, None),
    ("essentially", "adv", None, None, None, None, "về cơ bản, chủ yếu", "The idea is essentially correct.", None, None),
    ("establish", "verb", "established", "established", "establishing", None, "thành lập, thiết lập", "They established a new company.", None, None),
    ("establishment", "noun", None, None, None, None, "sự thành lập, cơ sở", "The establishment is old.", None, None),
    ("estate", "noun", None, None, None, None, "bất động sản, tài sản", "He owns a large estate.", None, None),
    ("estimate", "verb", "estimated", "estimated", "estimating", None, "ước tính, đánh giá", "She estimated the cost.", None, None),
    ("etc", "adv", None, None, None, None, "vân vân, và những thứ khác", "Bring paper, pens, etc.", None, None),
    ("ethics", "noun", None, None, None, None, "đạo đức, nguyên tắc", "He studies business ethics.", None, None),
    ("ethnic", "adj", None, None, None, None, "dân tộc, thuộc về dân tộc", "Vietnam is an ethnic country.", None, None),
    ("European", "adj", None, None, None, None, "người châu Âu, thuộc về châu Âu", "She is European.", None, None),
    ("evaluate", "verb", "evaluated", "evaluated", "evaluating", None, "đánh giá, ước lượng", "He evaluated the results.", None, None),
    ("evaluation", "noun", None, None, None, None, "sự đánh giá, ước lượng", "The evaluation was positive.", None, None),
    ("even", "adv", None, None, None, None, "thậm chí, ngay cả", "Even children can do this.", None, None),
    ("evening", "noun", None, None, None, None, "buổi tối", "We went for a walk in the evening.", None, None),
    ("event", "noun", None, None, None, None, "sự kiện, biến cố", "The event was successful.", None, None),
    ("eventually", "adv", None, None, None, None, "cuối cùng, rốt cuộc", "Eventually, he found a job.", None, None),
    ("ever", "adv", None, None, None, None, "bao giờ, từng", "Have you ever been to Paris?", None, None),
    ("every", "det", None, None, None, None, "mỗi, mọi", "Every student passed the test.", None, None),
    ("everybody", "pron", None, None, None, None, "mọi người", "Everybody is happy today.", None, None),
    ("everyday", "adj", None, None, None, None, "hàng ngày, thường ngày", "This is my everyday routine.", None, None),
    ("everyone", "pron", None, None, None, None, "mọi người, tất cả mọi người", "Everyone enjoyed the party.", None, None),
    ("everything", "pron", None, None, None, None, "mọi thứ, tất cả", "Everything is ready.", None, None),
    ("everywhere", "adv", None, None, None, None, "mọi nơi, khắp nơi", "We looked everywhere for the keys.", None, None),
    ("evidence", "noun", None, None, None, None, "bằng chứng, chứng cứ", "There is no evidence of crime.", None, None),
    ("evolution", "noun", None, None, None, None, "sự tiến hóa, phát triển", "Human evolution is fascinating.", None, None),
    ("evolve", "verb", "evolved", "evolved", "evolving", None, "tiến hóa, phát triển", "Species evolve over time.", None, None),
    ("exact", "adj", None, None, None, None, "chính xác, đúng", "The answer is exact.", None, None),
    ("exactly", "adv", None, None, None, None, "chính xác, đúng như vậy", "That's exactly what I meant.", None, None),
    ("examination", "noun", None, None, None, None, "kỳ thi, sự kiểm tra", "The examination was difficult.", None, None),
    ("examine", "verb", "examined", "examined", "examining", None, "kiểm tra, xem xét", "The doctor examined the patient.", None, None),
    ("example", "noun", None, None, None, None, "ví dụ, mẫu mực", "She gave an example.", None, None),
    ("exceed", "verb", "exceeded", "exceeded", "exceeding", None, "vượt quá, vượt lên", "The speed exceeded the limit.", None, None),
    ("excellent", "adj", None, None, None, None, "xuất sắc, tuyệt vời", "She is an excellent student.", None, None),
    ("except", "prep", None, None, None, None, "ngoại trừ, trừ ra", "Everyone is here except John.", None, None),
    ("exception", "noun", None, None, None, None, "ngoại lệ, trường hợp đặc biệt", "There is an exception to the rule.", None, None),
    ("exchange", "verb", "exchanged", "exchanged", "exchanging", None, "trao đổi, đổi", "They exchanged gifts.", None, None),
    ("exciting", "adj", None, None, None, None, "hào hứng, thú vị", "The movie was exciting.", None, None),
    ("executive", "noun", None, None, None, None, "giám đốc, người điều hành", "He is an executive at the company.", None, None),
    ("exercise", "noun", None, None, None, None, "bài tập, sự tập luyện", "Exercise is good for health.", None, None),
    ("exhibit", "verb", "exhibited", "exhibited", "exhibiting", None, "trưng bày, triển lãm", "The museum exhibited ancient artifacts.", None, None),
    ("exhibition", "noun", None, None, None, None, "cuộc triển lãm, trưng bày", "The exhibition was crowded.", None, None),
    ("exist", "verb", "existed", "existed", "existing", None, "tồn tại, hiện hữu", "Dinosaurs no longer exist.", None, None),
    ("existence", "noun", None, None, None, None, "sự tồn tại, hiện hữu", "The existence of life on Mars is unknown.", None, None),
    ("existing", "adj", None, None, None, None, "hiện tại, đang tồn tại", "The existing system is outdated.", None, None),
    ("expand", "verb", "expanded", "expanded", "expanding", None, "mở rộng, phát triển", "The company expanded overseas.", None, None),
    ("expansion", "noun", None, None, None, None, "sự mở rộng, phát triển", "The expansion was successful.", None, None),
    ("expect", "verb", "expected", "expected", "expecting", None, "mong đợi, kỳ vọng", "She expects good results.", None, None),
    ("expectation", "noun", None, None, None, None, "sự mong đợi, kỳ vọng", "His expectation was high.", None, None),
    ("expense", "noun", None, None, None, None, "chi phí, phí tổn", "Travel expense is high.", None, None),
    ("expensive", "adj", None, None, None, None, "đắt tiền, tốn kém", "The car is expensive.", None, None),
    ("experience", "noun", None, None, None, None, "kinh nghiệm, trải nghiệm", "She has a lot of experience.", None, None),
    ("experiment", "noun", None, None, None, None, "thí nghiệm, thử nghiệm", "The experiment failed.", None, None),
    ("expert", "noun", None, None, None, None, "chuyên gia, thành thạo", "He is an expert in math.", None, None),
    ("explain", "verb", "explained", "explained", "explaining", None, "giải thích, trình bày", "She explained the rules.", None, None),
    ("explanation", "noun", None, None, None, None, "sự giải thích, trình bày", "His explanation was clear.", None, None),
    ("explode", "verb", "exploded", "exploded", "exploding", None, "nổ, phát nổ", "The bomb exploded.", None, None),
    ("explore", "verb", "explored", "explored", "exploring", None, "khám phá, thăm dò", "They explored the cave.", None, None),
    ("explosion", "noun", None, None, None, None, "sự nổ, vụ nổ", "The explosion was loud.", None, None),
    ("expose", "verb", "exposed", "exposed", "exposing", None, "phơi bày, lộ ra", "The scandal was exposed.", None, None),
    ("exposure", "noun", None, None, None, None, "sự phơi bày, tiếp xúc", "Exposure to sunlight is healthy.", None, None),
    ("express", "verb", "expressed", "expressed", "expressing", None, "bày tỏ, biểu lộ", "She expressed her feelings.", None, None),
    ("expression", "noun", None, None, None, None, "biểu hiện, sự diễn đạt", "Her expression was sad.", None, None),
    ("extend", "verb", "extended", "extended", "extending", None, "mở rộng, kéo dài", "He extended his stay.", None, None),
    ("extension", "noun", None, None, None, None, "sự mở rộng, phần mở rộng", "The extension is complete.", None, None),
    ("extensive", "adj", None, None, None, None, "rộng rãi, bao quát", "The damage was extensive.", None, None),
    ("extent", "noun", None, None, None, None, "mức độ, phạm vi", "To some extent, he is right.", None, None),
    ("external", "adj", None, None, None, None, "bên ngoài, ngoại vi", "External factors affect results.", None, None),
    ("extra", "adj", None, None, None, None, "thêm, phụ", "She ordered extra food.", None, None),
    ("extraordinary", "adj", None, None, None, None, "phi thường, đặc biệt", "She has extraordinary talent.", None, None),
    ("extreme", "adj", None, None, None, None, "cực đoan, cực kỳ", "The weather is extreme.", None, None),
    ("extremely", "adv", None, None, None, None, "cực kỳ, vô cùng", "He is extremely smart.", None, None),
    ("eye", "noun", None, None, None, None, "mắt, con mắt", "She has blue eyes.", None, None),
    ("fabric", "noun", None, None, None, None, "vải, kết cấu", "The fabric is soft.", None, None),
    ("face", "noun", None, None, None, None, "khuôn mặt, đối mặt", "She washed her face.", None, None),
    ("facility", "noun", None, None, None, None, "cơ sở, tiện nghi", "The facility is modern.", None, None),
    ("fact", "noun", None, None, None, None, "sự thật, thực tế", "It is a fact.", None, None),
    ("factor", "noun", None, None, None, None, "yếu tố, nhân tố", "Many factors affect health.", None, None),
    ("factory", "noun", None, None, None, None, "nhà máy, xí nghiệp", "He works in a factory.", None, None),
    ("faculty", "noun", None, None, None, None, "giảng viên, khoa", "She is on the faculty.", None, None),
    ("fade", "verb", "faded", "faded", "fading", None, "phai màu, mờ dần", "The color faded.", None, None),
    ("fail", "verb", "failed", "failed", "failing", None, "thất bại, trượt", "He failed the test.", None, None),
    ("failure", "noun", None, None, None, None, "sự thất bại, hỏng", "Failure is a part of life.", None, None),
    ("fair", "adj", None, None, None, None, "công bằng, hợp lý", "The decision was fair.", None, None),
    ("fairly", "adv", None, None, None, None, "khá, một cách công bằng", "She was treated fairly.", None, None),
    ("faith", "noun", None, None, None, None, "niềm tin, tín ngưỡng", "She has faith in God.", None, None),
    ("fall", "verb", "fell", "fallen", "falling", None, "rơi, ngã", "The leaves fall in autumn.", None, None),
    ("false", "adj", None, None, None, None, "sai, giả", "The news was false.", None, None),
    ("familiar", "adj", None, None, None, None, "quen thuộc, thân thuộc", "The song sounds familiar.", None, None),
    ("family", "noun", None, None, None, None, "gia đình, họ hàng", "My family is large.", None, None),
    ("famous", "adj", None, None, None, None, "nổi tiếng, danh tiếng", "He is a famous singer.", None, None),
    ("fan", "noun", None, None, None, None, "người hâm mộ, quạt", "She is a football fan.", None, None),
    ("fantasy", "noun", None, None, None, None, "sự tưởng tượng, ảo tưởng", "He lives in a fantasy world.", None, None),
    ("far", "adv", None, None, None, None, "xa, xa xôi", "The school is far from home.", None, None),
    ("farm", "noun", None, None, None, None, "nông trại, trang trại", "He works on a farm.", None, None),
    ("farmer", "noun", None, None, None, None, "nông dân, người làm ruộng", "The farmer grows rice.", None, None),
    ("fashion", "noun", None, None, None, None, "thời trang, kiểu cách", "She loves fashion.", None, None),
    ("fast", "adj", None, None, None, None, "nhanh, mau", "He is a fast runner.", None, None),
    ("fat", "adj", None, None, None, None, "béo, mập", "The cat is fat.", None, None),
    ("fate", "noun", None, None, None, None, "số phận, định mệnh", "He believes in fate.", None, None),
    ("father", "noun", None, None, None, None, "cha, bố", "His father is a doctor.", None, None),
    ("fault", "noun", None, None, None, None, "lỗi, khuyết điểm", "It was not my fault.", None, None),
    ("favor", "noun", None, None, None, None, "ân huệ, sự giúp đỡ", "Can you do me a favor?", None, None),
    ("favorite", "adj", None, None, None, None, "yêu thích, ưa thích", "Blue is my favorite color.", None, None),
    ("fear", "noun", None, None, None, None, "nỗi sợ, sự lo lắng", "He has a fear of heights.", None, None),
    ("feature", "noun", None, None, None, None, "đặc điểm, tính năng", "This phone has many features.", None, None),
    ("federal", "adj", None, None, None, None, "liên bang, thuộc liên bang", "The federal government passed a law.", None, None),
    ("fee", "noun", None, None, None, None, "lệ phí, tiền thù lao", "The fee is $10.", None, None),
    ("feed", "verb", "fed", "fed", "feeding", None, "cho ăn, nuôi dưỡng", "She feeds the dog every morning.", None, None),
    ("feel", "verb", "felt", "felt", "feeling", None, "cảm thấy, cảm nhận", "I feel happy today.", None, None),
    ("feeling", "noun", None, None, None, None, "cảm giác, cảm xúc", "She has strong feelings.", None, None),
    ("fellow", "noun", None, None, None, None, "bạn, đồng nghiệp", "He is my fellow student.", None, None),
    ("female", "adj", None, None, None, None, "nữ, giống cái", "The female bird is smaller.", None, None),
    ("fence", "noun", None, None, None, None, "hàng rào, rào chắn", "The fence is made of wood.", None, None),
    ("few", "adj", None, None, None, None, "ít, một vài", "Few people know the answer.", None, None),
    ("fewer", "adj", None, None, None, None, "ít hơn, số lượng nhỏ hơn", "There are fewer cars today.", None, None),
    ("fiber", "noun", None, None, None, None, "chất xơ, sợi", "Fiber is good for health.", None, None),
    ("fiction", "noun", None, None, None, None, "tiểu thuyết, hư cấu", "She likes science fiction.", None, None),
    ("field", "noun", None, None, None, None, "cánh đồng, lĩnh vực", "He works in the medical field.", None, None),
    ("fifteen", "num", None, None, None, None, "mười lăm", "There are fifteen students.", None, None),
    ("fifth", "num", None, None, None, None, "thứ năm, số năm", "He finished fifth in the race.", None, None),
    ("fifty", "num", None, None, None, None, "năm mươi", "She is fifty years old.", None, None),
    ("fight", "verb", "fought", "fought", "fighting", None, "đánh nhau, chiến đấu", "They fought bravely.", None, None),
    ("fighter", "noun", None, None, None, None, "chiến binh, máy bay chiến đấu", "He is a fighter for justice.", None, None),
    ("fighting", "noun", None, None, None, None, "cuộc chiến, sự đánh nhau", "The fighting lasted for hours.", None, None),
    ("figure", "noun", None, None, None, None, "con số, hình dáng", "The figure is impressive.", None, None),
    ("file", "noun", None, None, None, None, "tập tin, hồ sơ", "Open the file on your computer.", None, None),
    ("fill", "verb", "filled", "filled", "filling", None, "làm đầy, điền vào", "She filled the glass with water.", None, None),
    ("film", "noun", None, None, None, None, "phim, cuộn phim", "We watched a film last night.", None, None),
    ("final", "adj", None, None, None, None, "cuối cùng, sau cùng", "This is the final exam.", None, None),
    ("finally", "adv", None, None, None, None, "cuối cùng, rốt cuộc", "He finally arrived.", None, None),
    ("finance", "noun", None, None, None, None, "tài chính, tiền bạc", "She works in finance.", None, None),
    ("financial", "adj", None, None, None, None, "thuộc về tài chính", "He has financial problems.", None, None),
    ("find", "verb", "found", "found", "finding", None, "tìm thấy, phát hiện", "She found her keys.", None, None),
    ("finding", "noun", None, None, None, None, "phát hiện, kết quả", "The finding was surprising.", None, None),
    ("fine", "adj", None, None, None, None, "tốt, ổn, đẹp", "The weather is fine today.", None, None),
    ("finger", "noun", None, None, None, None, "ngón tay", "She cut her finger.", None, None),
    ("finish", "verb", "finished", "finished", "finishing", None, "kết thúc, hoàn thành", "He finished his homework.", None, None),
    ("fire", "noun", None, None, None, None, "lửa, hỏa hoạn", "The fire was dangerous.", None, None),
    ("firm", "adj", None, None, None, None, "chắc chắn, kiên quyết", "She gave a firm answer.", None, None),
    ("first", "adj", None, None, None, None, "đầu tiên, thứ nhất", "He was the first to arrive.", None, None),
    ("fish", "noun", None, None, None, None, "cá, món cá", "She caught a big fish.", None, None),
    ("fishing", "noun", None, None, None, None, "câu cá, nghề cá", "Fishing is his hobby.", None, None),
    ("fit", "adj", None, None, None, None, "vừa vặn, phù hợp", "The shirt fits well.", None, None),
    ("fitness", "noun", None, None, None, None, "sự khỏe mạnh, thể hình", "He goes to the gym for fitness.", None, None),
    ("five", "num", None, None, None, None, "năm, số năm", "There are five apples.", None, None),
    ("fix", "verb", "fixed", "fixed", "fixing", None, "sửa chữa, cố định", "He fixed the broken chair.", None, None),
    ("flag", "noun", None, None, None, None, "cờ, lá cờ", "The flag is red and yellow.", None, None),
    ("flame", "noun", None, None, None, None, "ngọn lửa, ánh lửa", "The flame burned brightly.", None, None),
    ("flat", "adj", None, None, None, None, "phẳng, bằng phẳng", "The land is flat.", None, None),
    ("flavor", "noun", None, None, None, None, "hương vị, mùi vị", "This ice cream has a nice flavor.", None, None),
    ("flee", "verb", "fled", "fled", "fleeing", None, "chạy trốn, bỏ chạy", "They fled the country.", None, None),
    ("flesh", "noun", None, None, None, None, "thịt, da thịt", "The fruit has soft flesh.", None, None),
    ("flight", "noun", None, None, None, None, "chuyến bay, sự bay", "Her flight was delayed.", None, None),
    ("float", "verb", "floated", "floated", "floating", None, "nổi, trôi", "The boat floated on the lake.", None, None),
    ("floor", "noun", None, None, None, None, "sàn nhà, tầng", "The floor is clean.", None, None),
    ("flow", "verb", "flowed", "flowed", "flowing", None, "chảy, lưu thông", "The river flows quickly.", None, None),
    ("flower", "noun", None, None, None, None, "hoa, bông hoa", "She picked a flower.", None, None),
    ("fly", "verb", "flew", "flown", "flying", None, "bay, chuyến bay", "Birds fly in the sky.", None, None),
    ("focus", "verb", "focused", "focused", "focusing", None, "tập trung, chú ý", "She focused on her work.", None, None),
    ("folk", "noun", None, None, None, None, "dân gian, người dân", "Folk music is popular here.", None, None),
    ("follow", "verb", "followed", "followed", "following", None, "theo dõi, đi theo", "She followed the instructions.", None, None),
    ("following", "adj", None, None, None, None, "tiếp theo, sau đây", "The following day was sunny.", None, None),
    ("food", "noun", None, None, None, None, "thức ăn, thực phẩm", "She likes spicy food.", None, None),
    ("foot", "noun", None, None, None, None, "bàn chân, chân", "He hurt his foot.", None, None),
    ("football", "noun", None, None, None, None, "bóng đá, môn bóng đá", "He plays football every weekend.", None, None),
    ("for", "prep", None, None, None, None, "cho, vì, để", "This gift is for you.", None, None),
    ("force", "noun", None, None, None, None, "lực lượng, sức mạnh", "The police used force.", None, None),
    ("foreign", "adj", None, None, None, None, "nước ngoài, ngoại quốc", "She speaks foreign languages.", None, None),
    ("forest", "noun", None, None, None, None, "rừng, khu rừng", "The forest is dense.", None, None),
    ("forever", "adv", None, None, None, None, "mãi mãi, vĩnh viễn", "I will love you forever.", None, None),
    ("forget", "verb", "forgot", "forgotten", "forgetting", None, "quên, không nhớ", "She forgot her password.", None, None),
    ("form", "noun", None, None, None, None, "hình thức, mẫu đơn", "Fill out the form.", None, None),
    ("formal", "adj", None, None, None, None, "trang trọng, chính thức", "He wore formal clothes.", None, None),
    ("formation", "noun", None, None, None, None, "sự hình thành, cấu trúc", "The formation of clouds is interesting.", None, None),
    ("former", "adj", None, None, None, None, "trước đây, cũ", "He is a former president.", None, None),
    ("formula", "noun", None, None, None, None, "công thức, phương pháp", "The formula is simple.", None, None),
    ("forth", "adv", None, None, None, None, "về phía trước, ra ngoài", "He went forth into the world.", None, None),
    ("fortune", "noun", None, None, None, None, "vận may, tài sản", "She inherited a fortune.", None, None),
    ("forward", "adv", None, None, None, None, "phía trước, tiến lên", "Move forward quickly.", None, None),
    ("found", "verb", "found", "found", "finding", None, "tìm thấy, thành lập", "She found a new company.", None, None),
    ("foundation", "noun", None, None, None, None, "nền tảng, cơ sở", "Education is the foundation of success.", None, None),
    ("founder", "noun", None, None, None, None, "người sáng lập, người lập ra", "He is the founder of the business.", None, None),
    ("four", "num", None, None, None, None, "bốn, số bốn", "There are four chairs.", None, None),
    ("fourth", "num", None, None, None, None, "thứ tư, số bốn", "She finished fourth.", None, None),
    ("frame", "noun", None, None, None, None, "khung, sườn", "The picture frame is wooden.", None, None),
    ("framework", "noun", None, None, None, None, "khung, khuôn khổ", "The framework is strong.", None, None),
    ("free", "adj", None, None, None, None, "tự do, miễn phí", "The tickets are free.", None, None),
    ("freedom", "noun", None, None, None, None, "sự tự do, quyền tự do", "They fight for freedom.", None, None),
    ("freeze", "verb", "froze", "frozen", "freezing", None, "đóng băng, làm lạnh", "The lake froze in winter.", None, None),
    ("French", "adj", None, None, None, None, "người Pháp, thuộc về nước Pháp", "He is French.", None, None),
    ("frequency", "noun", None, None, None, None, "tần số, sự thường xuyên", "The frequency is high.", None, None),
    ("frequent", "adj", None, None, None, None, "thường xuyên, hay xảy ra", "He is a frequent visitor.", None, None),
    ("frequently", "adv", None, None, None, None, "thường xuyên, đều đặn", "She travels frequently.", None, None),
    ("fresh", "adj", None, None, None, None, "tươi, mới", "The bread is fresh.", None, None),
    ("friend", "noun", None, None, None, None, "bạn, người bạn", "He is my best friend.", None, None),
    ("friendly", "adj", None, None, None, None, "thân thiện, hiếu khách", "The staff are friendly.", None, None),
    ("friendship", "noun", None, None, None, None, "tình bạn, tình hữu nghị", "Their friendship is strong.", None, None),
    ("from", "prep", None, None, None, None, "từ, xuất phát từ", "She is from Vietnam.", None, None),
    ("front", "noun", None, None, None, None, "phía trước, mặt trước", "Stand at the front of the class.", None, None),
    ("fruit", "noun", None, None, None, None, "trái cây, quả", "She likes tropical fruit.", None, None),
    ("frustration", "noun", None, None, None, None, "sự thất vọng, nản lòng", "He felt frustration at work.", None, None),
    ("fuel", "noun", None, None, None, None, "nhiên liệu, chất đốt", "The car runs on fuel.", None, None),
    ("full", "adj", None, None, None, None, "đầy, no", "The glass is full.", None, None),
    ("fully", "adv", None, None, None, None, "hoàn toàn, đầy đủ", "She is fully aware.", None, None),
    ("fun", "noun", None, None, None, None, "vui vẻ, sự vui chơi", "The party was fun.", None, None),
    ("function", "noun", None, None, None, None, "chức năng, nhiệm vụ", "The function is important.", None, None),
    ("fund", "noun", None, None, None, None, "quỹ, nguồn vốn", "The fund supports education.", None, None),
    ("fundamental", "adj", None, None, None, None, "cơ bản, nền tảng", "This is a fundamental rule.", None, None),
    ("funding", "noun", None, None, None, None, "kinh phí, sự tài trợ", "The project needs funding.", None, None),
    ("funeral", "noun", None, None, None, None, "đám tang, lễ tang", "The funeral was sad.", None, None),
    ("funny", "adj", None, None, None, None, "buồn cười, hài hước", "The movie is funny.", None, None),
    ("furniture", "noun", None, None, None, None, "đồ nội thất, bàn ghế", "The furniture is new.", None, None),
    ("furthermore", "adv", None, None, None, None, "hơn nữa, ngoài ra", "Furthermore, he is smart.", None, None),
    ("future", "noun", None, None, None, None, "tương lai, về sau", "She plans for the future.", None, None),
    ("gain", "verb", "gained", "gained", "gaining", None, "đạt được, thu được", "She gained valuable experience.", None, None),
    ("galaxy", "noun", None, None, None, None, "thiên hà", "The Milky Way is a galaxy.", None, None),
    ("gallery", "noun", None, None, None, None, "phòng trưng bày, triển lãm", "We visited the art gallery.", None, None),
    ("game", "noun", None, None, None, None, "trò chơi, trận đấu", "He won the game.", None, None),
    ("gang", "noun", None, None, None, None, "băng nhóm, nhóm tội phạm", "The gang was arrested by police.", None, None),
    ("gap", "noun", None, None, None, None, "khoảng cách, lỗ hổng", "There is a gap between the two buildings.", None, None),
    ("garage", "noun", None, None, None, None, "nhà để xe, ga ra", "The car is parked in the garage.", None, None),
    ("garden", "noun", None, None, None, None, "vườn, khu vườn", "She grows flowers in her garden.", None, None),
    ("garlic", "noun", None, None, None, None, "tỏi", "Garlic adds flavor to food.", None, None),
    ("gas", "noun", None, None, None, None, "khí, xăng", "The car runs on gas.", None, None),
    ("gate", "noun", None, None, None, None, "cổng, cửa", "Open the gate for the guests.", None, None),
    ("gather", "verb", "gathered", "gathered", "gathering", None, "tập hợp, thu thập", "They gathered information for the report.", None, None),
    ("gay", "adj", None, None, None, None, "đồng tính, vui vẻ", "He is openly gay.", None, None),
    ("gaze", "verb", "gazed", "gazed", "gazing", None, "nhìn chằm chằm, ngắm", "She gazed at the stars.", None, None),
    ("gear", "noun", None, None, None, None, "bánh răng, thiết bị", "Change the gear in the car.", None, None),
    ("gender", "noun", None, None, None, None, "giới tính", "Gender equality is important.", None, None),
    ("gene", "noun", None, None, None, None, "gen, gen di truyền", "Genes determine traits.", None, None),
    ("general", "adj", None, None, None, None, "chung, tổng quát", "He gave a general overview.", None, None),
    ("generally", "adv", None, None, None, None, "nói chung, thường thường", "Generally, people like music.", None, None),
    ("generate", "verb", "generated", "generated", "generating", None, "tạo ra, sinh ra", "The machine generates electricity.", None, None),
    ("generation", "noun", None, None, None, None, "thế hệ, sự sinh ra", "The younger generation uses smartphones.", None, None),
    ("genetic", "adj", None, None, None, None, "di truyền, thuộc gen", "Genetic research is advanced.", None, None),
    ("gentleman", "noun", None, None, None, None, "quý ông, người lịch sự", "He is a true gentleman.", None, None),
    ("gently", "adv", None, None, None, None, "nhẹ nhàng, dịu dàng", "She spoke gently to the child.", None, None),
    ("German", "adj", None, None, None, None, "người Đức, thuộc về nước Đức", "He is German.", None, None),
    ("gesture", "noun", None, None, None, None, "cử chỉ, điệu bộ", "She made a friendly gesture.", None, None),
    ("get", "verb", "got", "gotten", "getting", None, "nhận, lấy, trở thành", "He got a new job.", None, None),
    ("ghost", "noun", None, None, None, None, "ma, hồn ma", "She saw a ghost in the house.", None, None),
    ("giant", "adj", None, None, None, None, "khổng lồ, to lớn", "The company is a giant in the industry.", None, None),
    ("gift", "noun", None, None, None, None, "quà tặng, năng khiếu", "She received a birthday gift.", None, None),
    ("gifted", "adj", None, None, None, None, "có năng khiếu, tài năng", "He is a gifted musician.", None, None),
    ("girl", "noun", None, None, None, None, "cô gái, bé gái", "The girl is playing outside.", None, None),
    ("girlfriend", "noun", None, None, None, None, "bạn gái", "His girlfriend is very kind.", None, None),
    ("give", "verb", "gave", "given", "giving", None, "cho, tặng, đưa ra", "She gave him a present.", None, None),
    ("given", "adj", None, None, None, None, "được cho, đã cho", "Given the situation, we must act.", None, None),
    ("glad", "adj", None, None, None, None, "vui mừng, hân hoan", "I am glad to see you.", None, None),
    ("glance", "verb", "glanced", "glanced", "glancing", None, "liếc nhìn, nhìn thoáng qua", "She glanced at her watch.", None, None),
    ("glass", "noun", None, None, None, None, "thủy tinh, ly", "The glass is full of water.", None, None),
    ("global", "adj", None, None, None, None, "toàn cầu, toàn thế giới", "Global warming is a concern.", None, None),
    ("glove", "noun", None, None, None, None, "găng tay", "She wore gloves in winter.", None, None),
    ("go", "verb", "went", "gone", "going", None, "đi, di chuyển", "They go to school every day.", None, None),
    ("goal", "noun", None, None, None, None, "mục tiêu, bàn thắng", "Her goal is to become a doctor.", None, None),
    ("God", "noun", None, None, None, None, "Chúa, thần thánh", "They pray to God.", None, None),
    ("gold", "noun", None, None, None, None, "vàng, kim loại quý", "The ring is made of gold.", None, None),
    ("golden", "adj", None, None, None, None, "bằng vàng, quý giá", "She has golden hair.", None, None),
    ("golf", "noun", None, None, None, None, "môn golf, chơi golf", "He plays golf on weekends.", None, None),
    ("good", "adj", None, None, None, None, "tốt, giỏi", "She is a good student.", None, None),
    ("government", "noun", None, None, None, None, "chính phủ, nhà nước", "The government passed a new law.", None, None),
    ("governor", "noun", None, None, None, None, "thống đốc, người đứng đầu", "He is the governor of the state.", None, None),
    ("grab", "verb", "grabbed", "grabbed", "grabbing", None, "chộp lấy, nắm lấy", "She grabbed her bag and left.", None, None),
    ("grade", "noun", None, None, None, None, "điểm số, cấp bậc", "He got a high grade in math.", None, None),
    ("gradually", "adv", None, None, None, None, "dần dần, từ từ", "The weather improved gradually.", None, None),
    ("graduate", "verb", "graduated", "graduated", "graduating", None, "tốt nghiệp, hoàn thành", "She graduated from university.", None, None),
    ("grain", "noun", None, None, None, None, "hạt, ngũ cốc", "Rice is a type of grain.", None, None),
    ("grand", "adj", None, None, None, None, "lớn, vĩ đại", "The hotel is very grand.", None, None),
    ("grandfather", "noun", None, None, None, None, "ông nội, ông ngoại", "My grandfather is 80 years old.", None, None),
    ("grandmother", "noun", None, None, None, None, "bà nội, bà ngoại", "Her grandmother lives in the countryside.", None, None),
    ("grant", "verb", "granted", "granted", "granting", None, "cấp, ban cho", "He was granted permission.", None, None),
    ("grass", "noun", None, None, None, None, "cỏ, bãi cỏ", "The grass is green.", None, None),
    ("grave", "noun", None, None, None, None, "mộ, phần mộ", "He visited his father's grave.", None, None),
    ("gray", "adj", None, None, None, None, "màu xám, bạc", "She has gray hair.", None, None),
    ("great", "adj", None, None, None, None, "tuyệt vời, lớn", "He did a great job.", None, None),
    ("greatest", "adj", None, None, None, None, "vĩ đại nhất, lớn nhất", "She is the greatest singer.", None, None),
    ("green", "adj", None, None, None, None, "màu xanh lá cây, tươi", "The leaves are green.", None, None),
    ("grocery", "noun", None, None, None, None, "cửa hàng tạp hóa, thực phẩm", "She went to the grocery store.", None, None),
    ("ground", "noun", None, None, None, None, "mặt đất, đất", "The ground is wet after rain.", None, None),
    ("group", "noun", None, None, None, None, "nhóm, tập thể", "They formed a study group.", None, None),
    ("grow", "verb", "grew", "grown", "growing", None, "phát triển, trồng", "She grows vegetables in her garden.", None, None),
    ("growing", "adj", None, None, None, None, "đang phát triển, tăng lên", "The company is growing rapidly.", None, None),
    ("growth", "noun", None, None, None, None, "sự phát triển, tăng trưởng", "The growth of the city is fast.", None, None),
    ("guarantee", "verb", "guaranteed", "guaranteed", "guaranteeing", None, "đảm bảo, cam kết", "The product is guaranteed for one year.", None, None),
    ("guard", "noun", None, None, None, None, "bảo vệ, lính canh", "The guard stood at the door.", None, None),
    ("guess", "verb", "guessed", "guessed", "guessing", None, "đoán, phỏng đoán", "Can you guess the answer?", None, None),
    ("guest", "noun", None, None, None, None, "khách, khách mời", "The guest arrived early.", None, None),
    ("guide", "noun", None, None, None, None, "hướng dẫn, người hướng dẫn", "The guide showed us around.", None, None),
    ("guideline", "noun", None, None, None, None, "hướng dẫn, quy định", "Follow the safety guidelines.", None, None),
    ("guilty", "adj", None, None, None, None, "có tội, cảm thấy tội lỗi", "He felt guilty about the mistake.", None, None),
    ("gun", "noun", None, None, None, None, "súng, vũ khí", "The police carry guns.", None, None),
    ("guy", "noun", None, None, None, None, "chàng trai, người đàn ông", "He is a nice guy.", None, None),
    ("habit", "noun", None, None, None, None, "thói quen, tập quán", "She has a habit of reading at night.", None, None),
    ("habitat", "noun", None, None, None, None, "môi trường sống, nơi cư trú", "The forest is a habitat for many animals.", None, None),
    ("hair", "noun", None, None, None, None, "tóc, mái tóc", "She has long hair.", None, None),
    ("half", "num", None, None, None, None, "một nửa, phân nửa", "Cut the apple in half.", None, None),
    ("hall", "noun", None, None, None, None, "hội trường, hành lang", "The meeting is in the main hall.", None, None),
    ("hand", "noun", None, None, None, None, "bàn tay, sự giúp đỡ", "She raised her hand.", None, None),
    ("handful", "noun", None, None, None, None, "một nắm, số ít", "He ate a handful of nuts.", None, None),
    ("handle", "verb", "handled", "handled", "handling", None, "xử lý, cầm nắm", "She handled the situation well.", None, None),
    ("hang", "verb", "hung", "hung", "hanging", None, "treo, mắc", "She hung the picture on the wall.", None, None),
    ("happen", "verb", "happened", "happened", "happening", None, "xảy ra, diễn ra", "What happened yesterday?", None, None),
    ("happy", "adj", None, None, None, None, "hạnh phúc, vui vẻ", "She is happy with her results.", None, None),
    ("hard", "adj", None, None, None, None, "cứng, khó khăn", "The exam was hard.", None, None),
    ("hardly", "adv", None, None, None, None, "hầu như không, hiếm khi", "She hardly goes out.", None, None),
    ("hat", "noun", None, None, None, None, "mũ, nón", "He wore a black hat.", None, None),
    ("hate", "verb", "hated", "hated", "hating", None, "ghét, căm ghét", "She hates waiting in line.", None, None),
    ("have", "verb", "had", "had", "having", None, "có, sở hữu", "I have a new phone.", None, None),
    ("he", "pron", None, None, None, None, "anh ấy, ông ấy", "He is my friend.", None, None),
    ("head", "noun", None, None, None, None, "đầu, lãnh đạo", "She hit her head on the door.", None, None),
    ("headline", "noun", None, None, None, None, "tiêu đề, dòng đầu", "The headline is bold.", None, None),
    ("headquarters", "noun", None, None, None, None, "trụ sở chính, tổng hành dinh", "The company headquarters is in Hanoi.", None, None),
    ("health", "noun", None, None, None, None, "sức khỏe, y tế", "Exercise is good for health.", None, None),
    ("healthy", "adj", None, None, None, None, "khỏe mạnh, lành mạnh", "She eats healthy food.", None, None),
    ("hear", "verb", "heard", "heard", "hearing", None, "nghe, lắng nghe", "Did you hear the news?", None, None),
    ("hearing", "noun", None, None, None, None, "thính giác, phiên tòa", "Her hearing is excellent.", None, None),
    ("heart", "noun", None, None, None, None, "trái tim, tấm lòng", "He has a kind heart.", None, None),
    ("heat", "noun", None, None, None, None, "nhiệt, hơi nóng", "The heat is intense today.", None, None),
    ("heaven", "noun", None, None, None, None, "thiên đường, trời", "She believes in heaven.", None, None),
    ("heavily", "adv", None, None, None, None, "nặng nề, nhiều", "It rained heavily last night.", None, None),
    ("heavy", "adj", None, None, None, None, "nặng, nặng nề", "The box is heavy.", None, None),
    ("heel", "noun", None, None, None, None, "gót chân, gót giày", "Her heel hurts.", None, None),
    ("height", "noun", None, None, None, None, "chiều cao, độ cao", "His height is above average.", None, None),
    ("helicopter", "noun", None, None, None, None, "trực thăng", "The helicopter landed safely.", None, None),
    ("hell", "noun", None, None, None, None, "địa ngục, nơi khổ sở", "He felt like he was in hell.", None, None),
    ("hello", "interj", None, None, None, None, "xin chào", "Hello, how are you?", None, None),
    ("help", "verb", "helped", "helped", "helping", None, "giúp đỡ, hỗ trợ", "She helped me with my homework.", None, None),
    ("helpful", "adj", None, None, None, None, "hữu ích, có ích", "The advice was helpful.", None, None),
    ("her", "pron", None, None, None, None, "cô ấy, của cô ấy", "Her book is on the table.", None, None),
    ("here", "adv", None, None, None, None, "ở đây, tại đây", "Come here, please.", None, None),
    ("heritage", "noun", None, None, None, None, "di sản, gia tài", "Vietnam has a rich heritage.", None, None),
    ("hero", "noun", None, None, None, None, "anh hùng, người hùng", "He is a national hero.", None, None),
    ("herself", "pron", None, None, None, None, "chính cô ấy, tự cô ấy", "She did it herself.", None, None),
    ("hey", "interj", None, None, None, None, "này, ê", "Hey, wait for me!", None, None),
    ("hi", "interj", None, None, None, None, "chào, xin chào", "Hi, nice to meet you!", None, None),
    ("hide", "verb", "hid", "hidden", "hiding", None, "giấu, trốn", "She hid the gift under the bed.", None, None),
    ("high", "adj", None, None, None, None, "cao, ở trên cao", "The mountain is very high.", None, None),
    ("highlight", "verb", "highlighted", "highlighted", "highlighting", None, "nhấn mạnh, làm nổi bật", "She highlighted the important points.", None, None),
    ("highly", "adv", None, None, None, None, "rất, hết sức", "She is highly skilled.", None, None),
    ("highway", "noun", None, None, None, None, "đường cao tốc, xa lộ", "The highway is busy.", None, None),
    ("hill", "noun", None, None, None, None, "đồi, gò", "They climbed the hill.", None, None),
    ("him", "pron", None, None, None, None, "anh ấy, ông ấy", "Give the book to him.", None, None),
    ("himself", "pron", None, None, None, None, "chính anh ấy, tự anh ấy", "He did it himself.", None, None),
    ("hip", "noun", None, None, None, None, "hông, eo", "She has a pain in her hip.", None, None),
    ("hire", "verb", "hired", "hired", "hiring", None, "thuê, tuyển dụng", "The company hired new staff.", None, None),
    ("his", "pron", None, None, None, None, "của anh ấy, của ông ấy", "His car is red.", None, None),
    ("historian", "noun", None, None, None, None, "nhà sử học", "He is a famous historian.", None, None),
    ("historic", "adj", None, None, None, None, "có tính lịch sử, quan trọng", "This is a historic event.", None, None),
    ("historical", "adj", None, None, None, None, "thuộc về lịch sử", "She studies historical documents.", None, None),
    ("history", "noun", None, None, None, None, "lịch sử, quá khứ", "He is interested in history.", None, None),
    ("hit", "verb", "hit", "hit", "hitting", None, "đánh, va chạm", "He hit the ball with a bat.", None, None),
    ("hold", "verb", "held", "held", "holding", None, "cầm, giữ, tổ chức", "She held the baby in her arms.", None, None),
    ("hole", "noun", None, None, None, None, "lỗ, hố", "There is a hole in the wall.", None, None),
    ("holiday", "noun", None, None, None, None, "ngày nghỉ, kỳ nghỉ", "They went on holiday to the beach.", None, None),
    ("holy", "adj", None, None, None, None, "thiêng liêng, thuộc về thần thánh", "The temple is a holy place.", None, None),
    ("home", "noun", None, None, None, None, "nhà, tổ ấm", "She feels safe at home.", None, None),
    ("homeless", "adj", None, None, None, None, "vô gia cư, không nhà cửa", "He helps homeless people.", None, None),
    ("honest", "adj", None, None, None, None, "trung thực, thật thà", "She is an honest person.", None, None),
    ("honey", "noun", None, None, None, None, "mật ong, người yêu", "She puts honey in her tea.", None, None),
    ("honor", "noun", None, None, None, None, "danh dự, vinh dự", "It is an honor to meet you.", None, None),
    ("hope", "verb", "hoped", "hoped", "hoping", None, "hy vọng, mong muốn", "I hope you have a good day.", None, None),
    ("horizon", "noun", None, None, None, None, "chân trời, phạm vi", "The sun set below the horizon.", None, None),
    ("horror", "noun", None, None, None, None, "kinh dị, sự kinh hoàng", "She likes horror movies.", None, None),
    ("horse", "noun", None, None, None, None, "con ngựa", "He rides a horse.", None, None),
    ("hospital", "noun", None, None, None, None, "bệnh viện", "She works at a hospital.", None, None),
    ("host", "noun", None, None, None, None, "chủ nhà, người dẫn chương trình", "He is the host of the show.", None, None),
    ("hot", "adj", None, None, None, None, "nóng, cay", "The soup is hot.", None, None),
    ("hotel", "noun", None, None, None, None, "khách sạn", "They stayed at a hotel.", None, None),
    ("hour", "noun", None, None, None, None, "giờ, tiếng đồng hồ", "The meeting lasted two hours.", None, None),
    ("house", "noun", None, None, None, None, "nhà, căn nhà", "She bought a new house.", None, None),
    ("household", "noun", None, None, None, None, "hộ gia đình, gia đình", "There are four people in the household.", None, None),
    ("housing", "noun", None, None, None, None, "nhà ở, chỗ ở", "The city needs more housing.", None, None),
    ("how", "adv", None, None, None, None, "như thế nào, làm sao", "How did you do that?", None, None),
    ("however", "adv", None, None, None, None, "tuy nhiên, dù thế nào", "However, I disagree.", None, None),
    ("huge", "adj", None, None, None, None, "to lớn, khổng lồ", "The building is huge.", None, None),
    ("human", "adj", None, None, None, None, "con người, thuộc về con người", "Human rights are important.", None, None),
    ("humor", "noun", None, None, None, None, "hài hước, sự hài hước", "He has a good sense of humor.", None, None),
    ("hundred", "num", None, None, None, None, "một trăm, số trăm", "There are a hundred students.", None, None),
    ("hungry", "adj", None, None, None, None, "đói, cảm thấy đói", "She is hungry after school.", None, None),
    ("hunter", "noun", None, None, None, None, "thợ săn, người săn bắn", "The hunter tracked the deer.", None, None),
    ("hunting", "noun", None, None, None, None, "săn bắn, cuộc săn", "Hunting is allowed in this area.", None, None),
    ("hurt", "verb", "hurt", "hurt", "hurting", None, "làm đau, bị thương", "He hurt his leg playing football.", None, None),
    ("husband", "noun", None, None, None, None, "chồng, người chồng", "Her husband is a doctor.", None, None),
    ("hypothesis", "noun", None, None, None, None, "giả thuyết, giả định", "The scientist tested the hypothesis.", None, None),
    ("I", "pron", None, None, None, None, "tôi, mình", "I am a student.", None, None),
    ("ice", "noun", None, None, None, None, "đá, băng", "She put ice in her drink.", None, None),
    ("idea", "noun", None, None, None, None, "ý tưởng, quan điểm", "He has a good idea.", None, None),
    ("ideal", "adj", None, None, None, None, "lý tưởng, hoàn hảo", "This is the ideal solution.", None, None),
    ("identification", "noun", None, None, None, None, "sự nhận dạng, giấy tờ tùy thân", "Show your identification at the entrance.", None, None),
    ("identify", "verb", "identified", "identified", "identifying", None, "nhận diện, xác định", "She identified the problem quickly.", None, None),
    ("identity", "noun", None, None, None, None, "bản sắc, danh tính", "He kept his identity secret.", None, None),
    ("ie", "adv", None, None, None, None, "tức là, nghĩa là", "He is a vegetarian, ie, he does not eat meat.", None, None),
    ("if", "conj", None, None, None, None, "nếu, giả sử", "If it rains, we will stay home.", None, None),
    ("ignore", "verb", "ignored", "ignored", "ignoring", None, "bỏ qua, phớt lờ", "She ignored his advice.", None, None),
    ("ill", "adj", None, None, None, None, "ốm, bệnh", "He is ill today.", None, None),
    ("illegal", "adj", None, None, None, None, "bất hợp pháp, trái luật", "It is illegal to steal.", None, None),
    ("illness", "noun", None, None, None, None, "bệnh, ốm đau", "She recovered from her illness.", None, None),
    ("illustrate", "verb", "illustrated", "illustrated", "illustrating", None, "minh họa, làm rõ", "The book is illustrated with pictures.", None, None),
    ("image", "noun", None, None, None, None, "hình ảnh, hình tượng", "She posted an image online.", None, None),
    ("imagination", "noun", None, None, None, None, "trí tưởng tượng, sự tưởng tượng", "Children have a vivid imagination.", None, None),
    ("imagine", "verb", "imagined", "imagined", "imagining", None, "tưởng tượng, hình dung", "Imagine a world without war.", None, None),
    ("immediate", "adj", None, None, None, None, "ngay lập tức, tức thì", "She needs immediate help.", None, None),
    ("immediately", "adv", None, None, None, None, "ngay lập tức, tức thì", "Call me immediately.", None, None),
    ("immigrant", "noun", None, None, None, None, "người nhập cư", "The city has many immigrants.", None, None),
    ("immigration", "noun", None, None, None, None, "sự nhập cư, di trú", "Immigration laws are strict.", None, None),
    ("impact", "noun", None, None, None, None, "tác động, ảnh hưởng", "The impact of the decision was huge.", None, None),
    ("implement", "verb", "implemented", "implemented", "implementing", None, "thực hiện, triển khai", "They implemented the new policy.", None, None),
    ("implication", "noun", None, None, None, None, "hàm ý, sự liên quan", "The implication is clear.", None, None),
    ("imply", "verb", "implied", "implied", "implying", None, "ngụ ý, ám chỉ", "Her words implied a warning.", None, None),
    ("importance", "noun", None, None, None, None, "tầm quan trọng", "Education is of great importance.", None, None),
    ("important", "adj", None, None, None, None, "quan trọng, thiết yếu", "This is an important meeting.", None, None),
    ("impose", "verb", "imposed", "imposed", "imposing", None, "áp đặt, bắt buộc", "The government imposed new rules.", None, None),
    ("impossible", "adj", None, None, None, None, "không thể, bất khả thi", "It is impossible to finish in one day.", None, None),
    ("impress", "verb", "impressed", "impressed", "impressing", None, "gây ấn tượng, làm cảm động", "She impressed everyone with her speech.", None, None),
    ("impression", "noun", None, None, None, None, "ấn tượng, cảm giác", "He made a good impression.", None, None),
    ("impressive", "adj", None, None, None, None, "ấn tượng, gây cảm giác mạnh", "Her performance was impressive.", None, None),
    ("improve", "verb", "improved", "improved", "improving", None, "cải thiện, tiến bộ", "She improved her English skills.", None, None),
    ("improvement", "noun", None, None, None, None, "sự cải thiện, tiến bộ", "There is a big improvement in quality.", None, None),
    ("in", "prep", None, None, None, None, "trong, ở", "She is in the room.", None, None),
    ("incentive", "noun", None, None, None, None, "động lực, khích lệ", "The company offers incentives.", None, None),
    ("incident", "noun", None, None, None, None, "sự việc, biến cố", "The incident happened last night.", None, None),
    ("include", "verb", "included", "included", "including", None, "bao gồm, kể cả", "The price includes tax.", None, None),
    ("including", "prep", None, None, None, None, "bao gồm, kể cả", "Everyone, including children, must attend.", None, None),
    ("income", "noun", None, None, None, None, "thu nhập, tiền lương", "Her income is high.", None, None),
    ("incorporate", "verb", "incorporated", "incorporated", "incorporating", None, "kết hợp, sát nhập", "The company incorporated new ideas.", None, None),
    ("increase", "verb", "increased", "increased", "increasing", None, "tăng, gia tăng", "Sales increased last month.", None, None),
    ("increased", "adj", None, None, None, None, "tăng lên, gia tăng", "There is increased demand.", None, None),
    ("increasing", "adj", None, None, None, None, "đang tăng lên, ngày càng tăng", "The population is increasing.", None, None),
    ("increasingly", "adv", None, None, None, None, "ngày càng, càng lúc càng", "It is increasingly difficult.", None, None),
    ("incredible", "adj", None, None, None, None, "khó tin, tuyệt vời", "Her talent is incredible.", None, None),
    ("indeed", "adv", None, None, None, None, "thật vậy, quả thật", "Indeed, you are right.", None, None),
    ("independence", "noun", None, None, None, None, "sự độc lập, tự chủ", "The country gained independence.", None, None),
    ("independent", "adj", None, None, None, None, "độc lập, tự chủ", "She is an independent woman.", None, None),
    ("index", "noun", None, None, None, None, "mục lục, chỉ số", "Check the index for details.", None, None),
    ("Indian", "adj", None, None, None, None, "người Ấn Độ, thuộc về Ấn Độ", "He is Indian.", None, None),
    ("indicate", "verb", "indicated", "indicated", "indicating", None, "chỉ ra, biểu thị", "The results indicate success.", None, None),
    ("indication", "noun", None, None, None, None, "dấu hiệu, sự chỉ dẫn", "There is no indication of rain.", None, None),
    ("individual", "noun", None, None, None, None, "cá nhân, riêng biệt", "Each individual is unique.", None, None),
    ("industrial", "adj", None, None, None, None, "thuộc về công nghiệp", "The city is an industrial center.", None, None),
    ("industry", "noun", None, None, None, None, "ngành công nghiệp, nghề", "The industry is growing.", None, None),
    ("infant", "noun", None, None, None, None, "trẻ sơ sinh, em bé", "The infant is sleeping.", None, None),
    ("infection", "noun", None, None, None, None, "nhiễm trùng, bệnh truyền nhiễm", "He has a throat infection.", None, None),
    ("inflation", "noun", None, None, None, None, "lạm phát, sự tăng giá", "Inflation affects prices.", None, None),
    ("influence", "noun", None, None, None, None, "ảnh hưởng, tác động", "She has a strong influence.", None, None),
    ("inform", "verb", "informed", "informed", "informing", None, "thông báo, báo tin", "She informed me of the changes.", None, None),
    ("information", "noun", None, None, None, None, "thông tin, dữ liệu", "The website provides information.", None, None),
    ("ingredient", "noun", None, None, None, None, "thành phần, nguyên liệu", "Salt is an ingredient in soup.", None, None),
    ("initial", "adj", None, None, None, None, "ban đầu, đầu tiên", "The initial results are good.", None, None),
    ("initially", "adv", None, None, None, None, "ban đầu, lúc đầu", "Initially, I was nervous.", None, None),
    ("initiative", "noun", None, None, None, None, "sáng kiến, sự chủ động", "She showed great initiative.", None, None),
    ("injury", "noun", None, None, None, None, "chấn thương, vết thương", "He has a leg injury.", None, None),
    ("inner", "adj", None, None, None, None, "bên trong, nội tâm", "She has inner strength.", None, None),
    ("innocent", "adj", None, None, None, None, "vô tội, ngây thơ", "The child is innocent.", None, None),
    ("inquiry", "noun", None, None, None, None, "cuộc điều tra, câu hỏi", "The police started an inquiry.", None, None),
    ("inside", "adv", None, None, None, None, "bên trong, phía trong", "The cat is inside the box.", None, None),
    ("insight", "noun", None, None, None, None, "cái nhìn sâu sắc, sự hiểu biết", "She gave insight into the problem.", None, None),
    ("insist", "verb", "insisted", "insisted", "insisting", None, "khăng khăng, nhấn mạnh", "She insisted on going.", None, None),
    ("inspire", "verb", "inspired", "inspired", "inspiring", None, "truyền cảm hứng, khích lệ", "Her story inspired many people.", None, None),
    ("install", "verb", "installed", "installed", "installing", None, "cài đặt, lắp đặt", "He installed the software.", None, None),
    ("instance", "noun", None, None, None, None, "trường hợp, ví dụ", "This is an instance of success.", None, None),
    ("instead", "adv", None, None, None, None, "thay vì, thay thế", "She stayed home instead of going out.", None, None),
    ("institution", "noun", None, None, None, None, "tổ chức, cơ quan", "The institution is well known.", None, None),
    ("institutional", "adj", None, None, None, None, "thuộc về tổ chức, cơ quan", "Institutional rules are strict.", None, None),
    ("instruction", "noun", None, None, None, None, "hướng dẫn, chỉ dẫn", "Follow the instructions carefully.", None, None),
    ("instructor", "noun", None, None, None, None, "giảng viên, người hướng dẫn", "He is a driving instructor.", None, None),
    ("instrument", "noun", None, None, None, None, "nhạc cụ, dụng cụ", "She plays a musical instrument.", None, None),
    ("insurance", "noun", None, None, None, None, "bảo hiểm, sự bảo đảm", "He bought health insurance.", None, None),
    ("intellectual", "adj", None, None, None, None, "trí tuệ, thuộc về trí tuệ", "He is an intellectual person.", None, None),
    ("intelligence", "noun", None, None, None, None, "trí thông minh, sự thông minh", "She has high intelligence.", None, None),
    ("intend", "verb", "intended", "intended", "intending", None, "dự định, có ý định", "She intends to travel abroad.", None, None),
    ("intense", "adj", None, None, None, None, "mãnh liệt, dữ dội", "The heat is intense.", None, None),
    ("intensity", "noun", None, None, None, None, "cường độ, độ mạnh", "The intensity of the light is high.", None, None),
    ("intention", "noun", None, None, None, None, "ý định, mục đích", "Her intention is clear.", None, None),
    ("interaction", "noun", None, None, None, None, "sự tương tác, giao tiếp", "Interaction between students is encouraged.", None, None),
    ("interest", "noun", None, None, None, None, "sở thích, sự quan tâm", "She has an interest in music.", None, None),
    ("interested", "adj", None, None, None, None, "quan tâm, thích thú", "He is interested in science.", None, None),
    ("interesting", "adj", None, None, None, None, "thú vị, hấp dẫn", "The book is interesting.", None, None),
    ("internal", "adj", None, None, None, None, "bên trong, nội bộ", "Internal problems need solutions.", None, None),
    ("international", "adj", None, None, None, None, "quốc tế, toàn cầu", "She works for an international company.", None, None),
    ("Internet", "noun", None, None, None, None, "mạng Internet", "The Internet is fast here.", None, None),
    ("interpret", "verb", "interpreted", "interpreted", "interpreting", None, "giải thích, phiên dịch", "She interpreted the message.", None, None),
    ("interpretation", "noun", None, None, None, None, "sự giải thích, sự phiên dịch", "Her interpretation was accurate.", None, None),
    ("intervention", "noun", None, None, None, None, "sự can thiệp, sự xen vào", "The doctor made an intervention.", None, None),
    ("interview", "noun", None, None, None, None, "cuộc phỏng vấn, phỏng vấn", "She had a job interview.", None, None),
    ("into", "prep", None, None, None, None, "vào trong, vào", "She walked into the room.", None, None),
    ("introduce", "verb", "introduced", "introduced", "introducing", None, "giới thiệu, đưa vào", "He introduced his friend.", None, None),
    ("introduction", "noun", None, None, None, None, "sự giới thiệu, phần mở đầu", "The introduction was brief.", None, None),
    ("invasion", "noun", None, None, None, None, "cuộc xâm lược, sự xâm chiếm", "The invasion lasted for months.", None, None),
    ("invest", "verb", "invested", "invested", "investing", None, "đầu tư, bỏ vốn", "She invested in stocks.", None, None),
    ("investigate", "verb", "investigated", "investigated", "investigating", None, "điều tra, nghiên cứu", "The police investigated the case.", None, None),
    ("investigation", "noun", None, None, None, None, "cuộc điều tra, sự nghiên cứu", "The investigation is ongoing.", None, None),
    ("investigator", "noun", None, None, None, None, "nhà điều tra, người điều tra", "He is a private investigator.", None, None),
    ("investment", "noun", None, None, None, None, "sự đầu tư, khoản đầu tư", "Her investment paid off.", None, None),
    ("investor", "noun", None, None, None, None, "nhà đầu tư", "The investor bought shares.", None, None),
    ("invite", "verb", "invited", "invited", "inviting", None, "mời, mời gọi", "She invited her friends.", None, None),
    ("involve", "verb", "involved", "involved", "involving", None, "liên quan, dính líu", "He was involved in the project.", None, None),
    ("involved", "adj", None, None, None, None, "liên quan, phức tạp", "The process is involved.", None, None),
    ("involvement", "noun", None, None, None, None, "sự tham gia, sự liên quan", "Her involvement was crucial.", None, None),
    ("Iraqi", "adj", None, None, None, None, "người Iraq, thuộc về Iraq", "He is Iraqi.", None, None),
    ("Irish", "adj", None, None, None, None, "người Ireland, thuộc về Ireland", "She is Irish.", None, None),
    ("iron", "noun", None, None, None, None, "sắt, bàn là", "The gate is made of iron.", None, None),
    ("Islamic", "adj", None, None, None, None, "Hồi giáo, thuộc về Hồi giáo", "He follows Islamic traditions.", None, None),
    ("island", "noun", None, None, None, None, "đảo, hòn đảo", "They live on an island.", None, None),
    ("Israeli", "adj", None, None, None, None, "người Israel, thuộc về Israel", "She is Israeli.", None, None),
    ("issue", "noun", None, None, None, None, "vấn đề, số phát hành", "This is a serious issue.", None, None),
    ("it", "pron", None, None, None, None, "nó, cái đó", "It is raining.", None, None),
    ("Italian", "adj", None, None, None, None, "người Ý, thuộc về nước Ý", "He is Italian.", None, None),
    ("item", "noun", None, None, None, None, "món đồ, mục", "She bought several items.", None, None),
    ("its", "pron", None, None, None, None, "của nó, thuộc về nó", "The dog wagged its tail.", None, None),
    ("itself", "pron", None, None, None, None, "chính nó, tự nó", "The cat cleaned itself.", None, None),
    ("jacket", "noun", None, None, None, None, "áo khoác, áo vét", "He wore a warm jacket.", None, None),
    ("jail", "noun", None, None, None, None, "nhà tù, tù", "He was sent to jail.", None, None),
    ("Japanese", "adj", None, None, None, None, "người Nhật, thuộc về Nhật Bản", "She is Japanese.", None, None),
    ("jet", "noun", None, None, None, None, "máy bay phản lực, tia nước", "The jet took off quickly.", None, None),
    ("Jew", "noun", None, None, None, None, "người Do Thái", "He is a Jew.", None, None),
    ("Jewish", "adj", None, None, None, None, "Do Thái, thuộc về Do Thái", "She is Jewish.", None, None),
    ("job", "noun", None, None, None, None, "công việc, nghề nghiệp", "He found a new job.", None, None),
    ("join", "verb", "joined", "joined", "joining", None, "tham gia, nối vào", "She joined the club.", None, None),
    ("joint", "adj", None, None, None, None, "chung, khớp", "They made a joint decision.", None, None),
    ("joke", "noun", None, None, None, None, "trò đùa, chuyện cười", "He told a funny joke.", None, None),
    ("journal", "noun", None, None, None, None, "tạp chí, nhật ký", "She writes in her journal.", None, None),
    ("journalist", "noun", None, None, None, None, "nhà báo, phóng viên", "He is a journalist.", None, None),
    ("journey", "noun", None, None, None, None, "chuyến đi, hành trình", "The journey took three days.", None, None),
    ("joy", "noun", None, None, None, None, "niềm vui, sự vui mừng", "She felt great joy.", None, None),
    ("judge", "noun", None, None, None, None, "thẩm phán, giám khảo", "The judge made a decision.", None, None),
    ("judgment", "noun", None, None, None, None, "sự phán xét, đánh giá", "Her judgment was fair.", None, None),
    ("juice", "noun", None, None, None, None, "nước ép, nước quả", "She drank orange juice.", None, None),
    ("jump", "verb", "jumped", "jumped", "jumping", None, "nhảy, bật lên", "He jumped over the fence.", None, None),
    ("junior", "adj", None, None, None, None, "trẻ, cấp dưới", "He is a junior employee.", None, None),
    ("jury", "noun", None, None, None, None, "ban giám khảo, hội đồng xét xử", "The jury found him guilty.", None, None),
    ("just", "adv", None, None, None, None, "chỉ, vừa mới", "She just arrived.", None, None),
    ("justice", "noun", None, None, None, None, "công lý, sự công bằng", "They fight for justice.", None, None),
    ("justify", "verb", "justified", "justified", "justifying", None, "biện minh, chứng minh", "She justified her actions.", None, None),
    ("keep", "verb", "kept", "kept", "keeping", None, "giữ, tiếp tục", "Keep the door closed.", None, None),
    ("key", "noun", None, None, None, None, "chìa khóa, quan trọng", "The key is on the table.", None, None),
    ("kick", "verb", "kicked", "kicked", "kicking", None, "đá, cú đá", "He kicked the ball.", None, None),
    ("kid", "noun", None, None, None, None, "trẻ em, đứa trẻ", "The kid is playing outside.", None, None),
    ("kill", "verb", "killed", "killed", "killing", None, "giết, tiêu diệt", "He killed the bug.", None, None),
    ("killer", "noun", None, None, None, None, "kẻ giết người, sát thủ", "The killer was caught.", None, None),
    ("killing", "noun", None, None, None, None, "vụ giết người, sự giết chóc", "The killing shocked the town.", None, None),
    ("kind", "adj", None, None, None, None, "tốt bụng, loại", "She is a kind person.", None, None),
    ("king", "noun", None, None, None, None, "vua, quốc vương", "The king ruled the country.", None, None),
    ("kiss", "verb", "kissed", "kissed", "kissing", None, "hôn, nụ hôn", "She kissed her baby.", None, None),
    ("kitchen", "noun", None, None, None, None, "nhà bếp, phòng bếp", "The kitchen is clean.", None, None),
    ("knee", "noun", None, None, None, None, "đầu gối", "He hurt his knee.", None, None),
    ("knife", "noun", None, None, None, None, "dao, lưỡi dao", "She cut the bread with a knife.", None, None),
    ("knock", "verb", "knocked", "knocked", "knocking", None, "gõ cửa, đánh", "He knocked on the door.", None, None),
    ("know", "verb", "knew", "known", "knowing", None, "biết, hiểu biết", "She knows the answer.", None, None),
    ("knowledge", "noun", None, None, None, None, "kiến thức, hiểu biết", "He has a lot of knowledge.", None, None),
    ("lab", "noun", None, None, None, None, "phòng thí nghiệm", "She works in a lab.", None, None),
    ("label", "noun", None, None, None, None, "nhãn, mác", "Read the label on the bottle.", None, None),
    ("labor", "noun", None, None, None, None, "lao động, công việc", "Labor is important for progress.", None, None),
    ("laboratory", "noun", None, None, None, None, "phòng thí nghiệm", "The laboratory is well equipped.", None, None),
    ("lack", "noun", None, None, None, None, "sự thiếu, thiếu hụt", "There is a lack of water.", None, None),
    ("lady", "noun", None, None, None, None, "quý bà, phụ nữ", "She is a kind lady.", None, None),
    ("lake", "noun", None, None, None, None, "hồ, ao", "They swam in the lake.", None, None),
    ("land", "noun", None, None, None, None, "đất, vùng đất", "He owns a lot of land.", None, None),
    ("landscape", "noun", None, None, None, None, "phong cảnh, cảnh quan", "The landscape is beautiful.", None, None),
    ("language", "noun", None, None, None, None, "ngôn ngữ, tiếng nói", "She speaks three languages.", None, None),
    ("lap", "noun", None, None, None, None, "vòng đua, lòng (đùi)", "The cat sat on her lap.", None, None),
    ("large", "adj", None, None, None, None, "lớn, rộng", "The house is large.", None, None),
    ("largely", "adv", None, None, None, None, "phần lớn, chủ yếu", "The success was largely due to teamwork.", None, None),
    ("last", "adj", None, None, None, None, "cuối cùng, vừa qua", "This is the last chance.", None, None),
    ("late", "adj", None, None, None, None, "muộn, trễ", "She arrived late.", None, None),
    ("later", "adv", None, None, None, None, "sau đó, muộn hơn", "We will meet later.", None, None),
    ("Latin", "adj", None, None, None, None, "tiếng Latin, thuộc về Latin", "She studies Latin language.", None, None),
    ("latter", "adj", None, None, None, None, "sau cùng, cái sau", "The latter option is better.", None, None),
    ("laugh", "verb", "laughed", "laughed", "laughing", None, "cười, tiếng cười", "She laughed at the joke.", None, None),
    ("launch", "verb", "launched", "launched", "launching", None, "phóng, ra mắt", "They launched a new product.", None, None),
    ("law", "noun", None, None, None, None, "luật, pháp luật", "He studies law at university.", None, None),
    ("lawn", "noun", None, None, None, None, "bãi cỏ, thảm cỏ", "The lawn is green.", None, None),
    ("lawsuit", "noun", None, None, None, None, "vụ kiện, kiện tụng", "She filed a lawsuit.", None, None),
    ("lawyer", "noun", None, None, None, None, "luật sư", "He is a famous lawyer.", None, None),
    ("lay", "verb", "laid", "laid", "laying", None, "đặt, để, nằm", "She laid the book on the table.", None, None),
    ("layer", "noun", None, None, None, None, "lớp, tầng", "There is a layer of dust.", None, None),
    ("lead", "verb", "led", "led", "leading", None, "dẫn dắt, chỉ huy", "She leads the team.", None, None),
    ("leader", "noun", None, None, None, None, "người lãnh đạo, thủ lĩnh", "He is a strong leader.", None, None),
    ("leadership", "noun", None, None, None, None, "khả năng lãnh đạo, sự lãnh đạo", "She has good leadership skills.", None, None),
    ("leading", "adj", None, None, None, None, "hàng đầu, dẫn đầu", "He is a leading expert.", None, None),
    ("leaf", "noun", None, None, None, None, "lá cây, tờ giấy", "The leaf fell from the tree.", None, None),
    ("league", "noun", None, None, None, None, "liên đoàn, giải đấu", "He plays in a football league.", None, None),
    ("lean", "verb", "leaned", "leaned", "leaning", None, "nghiêng, dựa vào", "She leaned against the wall.", None, None),
    ("learn", "verb", "learned", "learned", "learning", None, "học, tìm hiểu", "She learned French quickly.", None, None),
    ("learning", "noun", None, None, None, None, "việc học, kiến thức", "Learning is important for success.", None, None),
    ("least", "adv", None, None, None, None, "ít nhất, tối thiểu", "He has the least experience.", None, None),
    ("leather", "noun", None, None, None, None, "da, đồ da", "The bag is made of leather.", None, None),
    ("leave", "verb", "left", "left", "leaving", None, "rời đi, để lại", "She left the room.", None, None),
    ("left", "adj", None, None, None, None, "bên trái, còn lại", "The left side is damaged.", None, None),
    ("leg", "noun", None, None, None, None, "chân, cẳng chân", "He broke his leg.", None, None),
    ("legacy", "noun", None, None, None, None, "di sản, tài sản thừa kế", "He left a legacy for his children.", None, None),
    ("legal", "adj", None, None, None, None, "hợp pháp, thuộc pháp luật", "It is a legal business.", None, None),
    ("legend", "noun", None, None, None, None, "huyền thoại, truyền thuyết", "He is a football legend.", None, None),
    ("legislation", "noun", None, None, None, None, "pháp luật, sự lập pháp", "New legislation was passed.", None, None),
    ("legitimate", "adj", None, None, None, None, "hợp pháp, chính đáng", "He has a legitimate reason.", None, None),
    ("lemon", "noun", None, None, None, None, "quả chanh", "She added lemon to her tea.", None, None),
    ("length", "noun", None, None, None, None, "chiều dài, độ dài", "The length of the table is two meters.", None, None),
    ("less", "adj", None, None, None, None, "ít hơn, kém hơn", "He has less money than before.", None, None),
    ("lesson", "noun", None, None, None, None, "bài học, tiết học", "She learned a lesson.", None, None),
    ("let", "verb", "let", "let", "letting", None, "để cho, cho phép", "Let him try again.", None, None),
    ("letter", "noun", None, None, None, None, "lá thư, chữ cái", "She wrote a letter.", None, None),
    ("level", "noun", None, None, None, None, "mức độ, cấp độ", "Her English level is high.", None, None),
    ("liberal", "adj", None, None, None, None, "tự do, rộng rãi", "He has liberal views.", None, None),
    ("library", "noun", None, None, None, None, "thư viện", "She studies at the library.", None, None),
    ("license", "noun", None, None, None, None, "giấy phép, bằng cấp", "He got his driver's license.", None, None),
    ("lie", "verb", "lay", "lain", "lying", None, "nằm, nói dối", "He lay on the bed.", None, None),
    ("life", "noun", None, None, None, None, "cuộc sống, đời sống", "She enjoys life.", None, None),
    ("lifestyle", "noun", None, None, None, None, "phong cách sống, lối sống", "He has a healthy lifestyle.", None, None),
    ("lifetime", "noun", None, None, None, None, "cả đời, suốt đời", "She worked there for a lifetime.", None, None),
    ("lift", "verb", "lifted", "lifted", "lifting", None, "nâng lên, nhấc lên", "He lifted the box.", None, None),
    ("light", "noun", None, None, None, None, "ánh sáng, đèn", "Turn on the light.", None, None),
    ("like", "verb", "liked", "liked", "liking", None, "thích, giống như", "She likes chocolate.", None, None),
    ("likely", "adj", None, None, None, None, "có khả năng, có thể", "It is likely to rain.", None, None),
    ("limit", "noun", None, None, None, None, "giới hạn, hạn chế", "There is a limit to everything.", None, None),
    ("limitation", "noun", None, None, None, None, "sự hạn chế, giới hạn", "The project has some limitations.", None, None),
    ("limited", "adj", None, None, None, None, "bị hạn chế, có giới hạn", "The offer is limited.", None, None),
    ("line", "noun", None, None, None, None, "dòng, hàng, đường kẻ", "Stand in line.", None, None),
    ("link", "noun", None, None, None, None, "liên kết, đường dẫn", "Click the link to open the page.", None, None),
    ("lip", "noun", None, None, None, None, "môi, viền", "She put lipstick on her lip.", None, None),
    ("list", "noun", None, None, None, None, "danh sách, liệt kê", "She made a shopping list.", None, None),
    ("listen", "verb", "listened", "listened", "listening", None, "nghe, lắng nghe", "Listen to the music.", None, None),
    ("literally", "adv", None, None, None, None, "theo nghĩa đen, thực sự", "She literally jumped for joy.", None, None),
    ("literary", "adj", None, None, None, None, "văn học, thuộc về văn học", "She is a literary critic.", None, None),
    ("literature", "noun", None, None, None, None, "văn học, tác phẩm văn học", "He studies English literature.", None, None),
    ("little", "adj", None, None, None, None, "nhỏ, ít", "She has little money.", None, None),
    ("live", "verb", "lived", "lived", "living", None, "sống, tồn tại", "They live in Hanoi.", None, None),
    ("living", "adj", None, None, None, None, "đang sống, sinh động", "She is a living legend.", None, None),
    ("load", "verb", "loaded", "loaded", "loading", None, "chất lên, tải", "He loaded the truck.", None, None),
    ("loan", "noun", None, None, None, None, "khoản vay, cho vay", "She got a bank loan.", None, None),
    ("local", "adj", None, None, None, None, "địa phương, thuộc địa phương", "She buys local products.", None, None),
    ("locate", "verb", "located", "located", "locating", None, "định vị, xác định vị trí", "She located the missing keys.", None, None),
    ("location", "noun", None, None, None, None, "vị trí, địa điểm", "The location is perfect.", None, None),
    ("lock", "verb", "locked", "locked", "locking", None, "khóa, chốt", "She locked the door.", None, None),
    ("long", "adj", None, None, None, None, "dài, lâu", "The road is long.", None, None),
    ("long-term", "adj", None, None, None, None, "dài hạn, lâu dài", "They have a long-term plan.", None, None),
    ("look", "verb", "looked", "looked", "looking", None, "nhìn, xem", "Look at the sky.", None, None),
    ("loose", "adj", None, None, None, None, "lỏng, không chặt", "The shirt is loose.", None, None),
    ("lose", "verb", "lost", "lost", "losing", None, "mất, thua", "She lost her wallet.", None, None),
    ("loss", "noun", None, None, None, None, "sự mất mát, thua lỗ", "The company suffered a loss.", None, None),
    ("lost", "adj", None, None, None, None, "bị mất, lạc", "He is lost in the city.", None, None),
    ("lot", "noun", None, None, None, None, "nhiều, lô đất", "She has a lot of friends.", None, None),
    ("lots", "noun", None, None, None, None, "nhiều, số lượng lớn", "There are lots of options.", None, None),
    ("loud", "adj", None, None, None, None, "to, ồn ào", "The music is loud.", None, None),
    ("love", "noun", None, None, None, None, "tình yêu, yêu thương", "She is in love.", None, None),
    ("lovely", "adj", None, None, None, None, "đáng yêu, dễ thương", "She has a lovely smile.", None, None),
    ("lover", "noun", None, None, None, None, "người yêu, tình nhân", "He is her lover.", None, None),
    ("low", "adj", None, None, None, None, "thấp, nhỏ", "The price is low.", None, None),
    ("lower", "verb", "lowered", "lowered", "lowering", None, "hạ xuống, giảm xuống", "She lowered her voice.", None, None),
    ("luck", "noun", None, None, None, None, "may mắn, vận may", "He has good luck.", None, None),
    ("lucky", "adj", None, None, None, None, "may mắn, gặp may", "She is lucky to win.", None, None),
    ("lunch", "noun", None, None, None, None, "bữa trưa", "They had lunch together.", None, None),
    ("lung", "noun", None, None, None, None, "phổi, lá phổi", "Smoking damages the lungs.", None, None),
    ("machine", "noun", None, None, None, None, "máy móc, thiết bị", "The washing machine is new.", None, None),
    ("mad", "adj", None, None, None, None, "điên, tức giận", "He is mad about the mistake.", None, None),
    ("magazine", "noun", None, None, None, None, "tạp chí, báo", "She reads a fashion magazine.", None, None),
    ("mail", "noun", None, None, None, None, "thư, bưu kiện", "She sent the mail yesterday.", None, None),
    ("main", "adj", None, None, None, None, "chính, chủ yếu", "The main reason is cost.", None, None),
    ("mainly", "adv", None, None, None, None, "chủ yếu, phần lớn", "The group is mainly students.", None, None),
    ("maintain", "verb", "maintained", "maintained", "maintaining", None, "duy trì, bảo trì", "She maintains her car well.", None, None),
    ("maintenance", "noun", None, None, None, None, "bảo trì, sự duy trì", "The machine needs maintenance.", None, None),
    ("major", "adj", None, None, None, None, "chính, lớn, chuyên ngành", "Her major is biology.", None, None),
    ("majority", "noun", None, None, None, None, "đa số, phần lớn", "The majority agreed.", None, None),
    ("make", "verb", "made", "made", "making", None, "làm, tạo ra", "She made a cake.", None, None),
    ("maker", "noun", None, None, None, None, "người làm, nhà sản xuất", "He is a furniture maker.", None, None),
    ("makeup", "noun", None, None, None, None, "trang điểm, sự trang điểm", "She wears makeup every day.", None, None),
    ("male", "adj", None, None, None, None, "nam, giống đực", "The male bird is colorful.", None, None),
    ("mall", "noun", None, None, None, None, "trung tâm mua sắm", "They went to the mall.", None, None),
    ("man", "noun", None, None, None, None, "đàn ông, con người", "He is a strong man.", None, None),
    ("manage", "verb", "managed", "managed", "managing", None, "quản lý, xoay sở", "She manages a team.", None, None),
    ("management", "noun", None, None, None, None, "quản lý, ban quản lý", "Management made the decision.", None, None),
    ("manager", "noun", None, None, None, None, "quản lý, người quản lý", "He is the manager of the store.", None, None),
    ("manner", "noun", None, None, None, None, "cách thức, thái độ", "She spoke in a polite manner.", None, None),
    ("manufacturer", "noun", None, None, None, None, "nhà sản xuất, hãng sản xuất", "The manufacturer makes cars.", None, None),
    ("manufacturing", "noun", None, None, None, None, "sản xuất, ngành sản xuất", "Manufacturing is important for the economy.", None, None),
    ("many", "adj", None, None, None, None, "nhiều, số nhiều", "Many people attended the event.", None, None),
    ("map", "noun", None, None, None, None, "bản đồ", "She looked at the map.", None, None),
    ("margin", "noun", None, None, None, None, "lề, biên, lợi nhuận", "The margin is small.", None, None),
    ("mark", "verb", "marked", "marked", "marking", None, "đánh dấu, ghi chú", "She marked the date on her calendar.", None, None),
    ("market", "noun", None, None, None, None, "chợ, thị trường", "She sells fruit at the market.", None, None),
    ("marketing", "noun", None, None, None, None, "tiếp thị, quảng cáo", "She works in marketing.", None, None),
    ("marriage", "noun", None, None, None, None, "hôn nhân, lễ cưới", "Their marriage is happy.", None, None),
    ("married", "adj", None, None, None, None, "đã kết hôn, cưới", "She is married.", None, None),
    ("marry", "verb", "married", "married", "marrying", None, "kết hôn, cưới", "They will marry next year.", None, None),
    ("mask", "noun", None, None, None, None, "mặt nạ, khẩu trang", "She wore a mask.", None, None),
    ("mass", "noun", None, None, None, None, "khối lượng, số đông", "The mass of the object is 5 kg.", None, None),
    ("massive", "adj", None, None, None, None, "to lớn, đồ sộ", "The building is massive.", None, None),
    ("master", "noun", None, None, None, None, "bậc thầy, chủ nhân", "He is a chess master.", None, None),
    ("match", "noun", None, None, None, None, "trận đấu, que diêm", "The match ended in a draw.", None, None),
    ("material", "noun", None, None, None, None, "vật liệu, tài liệu", "The material is strong.", None, None),
    ("math", "noun", None, None, None, None, "toán học, môn toán", "She studies math.", None, None),
    ("matter", "noun", None, None, None, None, "vấn đề, chất", "It doesn't matter.", None, None),
    ("may", "verb", "might", "might", "maying", None, "có thể, được phép", "You may leave now.", None, None),
    ("maybe", "adv", None, None, None, None, "có lẽ, có thể", "Maybe it will rain.", None, None),
    ("mayor", "noun", None, None, None, None, "thị trưởng", "He is the mayor of the city.", None, None),
    ("me", "pron", None, None, None, None, "tôi, mình", "Give it to me.", None, None),
    ("meal", "noun", None, None, None, None, "bữa ăn, bữa cơm", "She cooked a meal.", None, None),
    ("mean", "verb", "meant", "meant", "meaning", None, "có nghĩa, ý định", "What does this word mean?", None, None),
    ("meaning", "noun", None, None, None, None, "ý nghĩa, nghĩa", "The meaning is clear.", None, None),
    ("meanwhile", "adv", None, None, None, None, "trong lúc đó, trong khi", "Meanwhile, she finished her work.", None, None),
    ("measure", "verb", "measured", "measured", "measuring", None, "đo lường, biện pháp", "She measured the length.", None, None),
    ("measurement", "noun", None, None, None, None, "sự đo lường, kích thước", "The measurement is accurate.", None, None),
    ("meat", "noun", None, None, None, None, "thịt, thịt động vật", "She doesn't eat meat.", None, None),
    ("mechanism", "noun", None, None, None, None, "cơ chế, máy móc", "The mechanism is complex.", None, None),
    ("media", "noun", None, None, None, None, "truyền thông, phương tiện", "She works in media.", None, None),
    ("medical", "adj", None, None, None, None, "y tế, thuộc về y tế", "She has medical insurance.", None, None),
    ("medication", "noun", None, None, None, None, "thuốc, sự điều trị", "She takes medication daily.", None, None),
    ("medicine", "noun", None, None, None, None, "thuốc, y học", "She studies medicine.", None, None),
    ("medium", "noun", None, None, None, None, "trung bình, phương tiện", "The medium is oil paint.", None, None),
    ("meet", "verb", "met", "met", "meeting", None, "gặp gỡ, họp", "She met her friend.", None, None),
    ("meeting", "noun", None, None, None, None, "cuộc họp, gặp mặt", "The meeting is at 10 AM.", None, None),
    ("member", "noun", None, None, None, None, "thành viên, hội viên", "She is a member of the club.", None, None),
    ("membership", "noun", None, None, None, None, "tư cách thành viên, hội viên", "Her membership is valid.", None, None),
    ("memory", "noun", None, None, None, None, "ký ức, trí nhớ", "She has a good memory.", None, None),
    ("mental", "adj", None, None, None, None, "tinh thần, tâm thần", "She has mental strength.", None, None),
    ("mention", "verb", "mentioned", "mentioned", "mentioning", None, "đề cập, nhắc đến", "She mentioned the problem.", None, None),
    ("menu", "noun", None, None, None, None, "thực đơn, bảng chọn", "She looked at the menu.", None, None),
    ("mere", "adj", None, None, None, None, "chỉ là, đơn thuần", "It was a mere accident.", None, None),
    ("merely", "adv", None, None, None, None, "chỉ, đơn thuần", "She was merely tired.", None, None),
    ("mess", "noun", None, None, None, None, "lộn xộn, hỗn độn", "The room is a mess.", None, None),
    ("message", "noun", None, None, None, None, "tin nhắn, thông điệp", "She sent a message.", None, None),
    ("metal", "noun", None, None, None, None, "kim loại, sắt thép", "The table is made of metal.", None, None),
    ("meter", "noun", None, None, None, None, "mét, đồng hồ đo", "The meter shows the distance.", None, None),
    ("method", "noun", None, None, None, None, "phương pháp, cách thức", "She used a new method.", None, None),
    ("Mexican", "adj", None, None, None, None, "người Mexico, thuộc về Mexico", "He is Mexican.", None, None),
    ("middle", "noun", None, None, None, None, "giữa, trung tâm", "She stood in the middle.", None, None),
    ("might", "verb", "might", "might", "mighting", None, "có thể, có khả năng", "It might rain today.", None, None),
    ("military", "adj", None, None, None, None, "quân sự, thuộc về quân đội", "He is in the military.", None, None),
    ("milk", "noun", None, None, None, None, "sữa, sữa động vật", "She drinks milk every morning.", None, None),
    ("million", "num", None, None, None, None, "một triệu, số triệu", "The company made a million dollars.", None, None),
    ("mind", "noun", None, None, None, None, "tâm trí, ý kiến", "She changed her mind.", None, None),
    ("mine", "pron", None, None, None, None, "của tôi, mỏ", "This book is mine.", None, None),
    ("minister", "noun", None, None, None, None, "bộ trưởng, mục sư", "He is a government minister.", None, None),
    ("minor", "adj", None, None, None, None, "nhỏ, không quan trọng", "It was a minor mistake.", None, None),
    ("minority", "noun", None, None, None, None, "thiểu số, số ít", "They are a minority group.", None, None),
    ("minute", "noun", None, None, None, None, "phút, khoảnh khắc", "Wait a minute.", None, None),
    ("miracle", "noun", None, None, None, None, "phép màu, kỳ diệu", "It was a miracle.", None, None),
    ("mirror", "noun", None, None, None, None, "gương, soi gương", "She looked in the mirror.", None, None),
    ("miss", "verb", "missed", "missed", "missing", None, "nhớ, bỏ lỡ", "She missed the bus.", None, None),
    ("missile", "noun", None, None, None, None, "tên lửa, vật phóng", "The missile was launched.", None, None),
    ("mission", "noun", None, None, None, None, "nhiệm vụ, sứ mệnh", "Her mission is to help others.", None, None),
    ("mistake", "noun", None, None, None, None, "lỗi, sai lầm", "She made a mistake.", None, None),
    ("mix", "verb", "mixed", "mixed", "mixing", None, "trộn, pha trộn", "She mixed the ingredients.", None, None),
    ("mixture", "noun", None, None, None, None, "hỗn hợp, sự pha trộn", "The mixture is ready.", None, None),
    ("mm-hmm", "interj", None, None, None, None, "ừ, vâng", "Mm-hmm, I agree.", None, None),
    ("mode", "noun", None, None, None, None, "chế độ, cách thức", "Switch to silent mode.", None, None),
    ("model", "noun", None, None, None, None, "mẫu, người mẫu", "She is a fashion model.", None, None),
    ("moderate", "adj", None, None, None, None, "vừa phải, ôn hòa", "She has moderate views.", None, None),
    ("modern", "adj", None, None, None, None, "hiện đại, mới", "The house is modern.", None, None),
    ("modest", "adj", None, None, None, None, "khiêm tốn, giản dị", "She is modest about her success.", None, None),
    ("mom", "noun", None, None, None, None, "mẹ, má", "Her mom is a nurse.", None, None),
    ("moment", "noun", None, None, None, None, "khoảnh khắc, phút chốc", "It was a happy moment.", None, None),
    ("money", "noun", None, None, None, None, "tiền, tiền bạc", "She saved money for a trip.", None, None),
    ("monitor", "noun", None, None, None, None, "màn hình, giám sát", "She looked at the monitor.", None, None),
    ("month", "noun", None, None, None, None, "tháng, thời gian", "She was born in May, a month of spring.", None, None),
    ("mood", "noun", None, None, None, None, "tâm trạng, cảm xúc", "She is in a good mood.", None, None),
    ("moon", "noun", None, None, None, None, "mặt trăng, trăng", "The moon is bright tonight.", None, None),
    ("moral", "adj", None, None, None, None, "đạo đức, luân lý", "She has strong moral values.", None, None),
    ("more", "adv", None, None, None, None, "hơn, thêm nữa", "She wants more time.", None, None),
    ("moreover", "adv", None, None, None, None, "hơn nữa, ngoài ra", "Moreover, he is talented.", None, None),
    ("morning", "noun", None, None, None, None, "buổi sáng, sáng", "She wakes up early in the morning.", None, None),
    ("mortgage", "noun", None, None, None, None, "thế chấp, khoản vay thế chấp", "She paid off her mortgage.", None, None),
    ("most", "adv", None, None, None, None, "hầu hết, phần lớn", "Most people agree.", None, None),
    ("mostly", "adv", None, None, None, None, "chủ yếu, phần lớn", "She eats mostly vegetables.", None, None),
    ("mother", "noun", None, None, None, None, "mẹ, mẫu thân", "Her mother is a teacher.", None, None),
    ("motion", "noun", None, None, None, None, "chuyển động, động tác", "The motion was fast.", None, None),
    ("motivation", "noun", None, None, None, None, "động lực, sự thúc đẩy", "She has strong motivation.", None, None),
    ("motor", "noun", None, None, None, None, "động cơ, mô tơ", "The motor is powerful.", None, None),
    ("mount", "verb", "mounted", "mounted", "mounting", None, "gắn, leo lên", "She mounted the horse.", None, None),
    ("mountain", "noun", None, None, None, None, "núi, ngọn núi", "They climbed the mountain.", None, None),
    ("mouse", "noun", None, None, None, None, "chuột, con chuột", "She saw a mouse in the kitchen.", None, None),
    ("mouth", "noun", None, None, None, None, "miệng, cửa miệng", "She brushed her mouth.", None, None),
    ("move", "verb", "moved", "moved", "moving", None, "di chuyển, chuyển nhà", "She moved to a new city.", None, None),
    ("movement", "noun", None, None, None, None, "sự chuyển động, phong trào", "The movement gained support.", None, None),
    ("movie", "noun", None, None, None, None, "phim, bộ phim", "She watched a movie.", None, None),
    ("Mr", "noun", None, None, None, None, "ông, ngài", "Mr. Smith is my teacher.", None, None),
    ("Mrs", "noun", None, None, None, None, "bà, phu nhân", "Mrs. Brown is kind.", None, None),
    ("Ms", "noun", None, None, None, None, "cô, bà", "Ms. Lee is my boss.", None, None),
    ("much", "adv", None, None, None, None, "nhiều, lắm", "She doesn't have much time.", None, None),
    ("multiple", "adj", None, None, None, None, "nhiều, đa dạng", "She has multiple talents.", None, None),
    ("murder", "noun", None, None, None, None, "giết người, vụ giết người", "The murder shocked the city.", None, None),
    ("muscle", "noun", None, None, None, None, "cơ bắp, sức mạnh", "He has strong muscles.", None, None),
    ("museum", "noun", None, None, None, None, "bảo tàng, viện bảo tàng", "She visited the museum.", None, None),
    ("music", "noun", None, None, None, None, "âm nhạc, bài hát", "She listens to music.", None, None),
    ("musical", "adj", None, None, None, None, "thuộc về âm nhạc, nhạc kịch", "She likes musical shows.", None, None),
    ("musician", "noun", None, None, None, None, "nhạc sĩ, người chơi nhạc", "He is a talented musician.", None, None),
    ("Muslim", "noun", None, None, None, None, "người Hồi giáo, thuộc về Hồi giáo", "He is a Muslim.", None, None),
    ("must", "verb", "had to", "had to", "musting", None, "phải, cần phải", "You must study hard.", None, None),
     ("mutual", "adj", None, None, None, None, "lẫn nhau, chung", "They have mutual respect.", None, None),
    ("my", "pron", None, None, None, None, "của tôi, của mình", "My house is big.", None, None),
    ("myself", "pron", None, None, None, None, "chính tôi, tự tôi", "I did it myself.", None, None),
    ("mystery", "noun", None, None, None, None, "bí ẩn, điều bí ẩn", "The story is a mystery.", None, None),
    ("myth", "noun", None, None, None, None, "thần thoại, chuyện hoang đường", "She studies Greek myth.", None, None),
    ("name", "noun", None, None, None, None, "tên, danh xưng", "Her name is Anna.", None, None),
    ("narrative", "noun", None, None, None, None, "tường thuật, chuyện kể", "She wrote a narrative.", None, None),
    ("narrow", "adj", None, None, None, None, "hẹp, chật", "The street is narrow.", None, None),
    ("nation", "noun", None, None, None, None, "quốc gia, dân tộc", "Vietnam is a nation.", None, None),
    ("national", "adj", None, None, None, None, "quốc gia, thuộc về quốc gia", "She is a national hero.", None, None),
    ("native", "adj", None, None, None, None, "bản địa, quê hương", "She is a native speaker.", None, None),
    ("natural", "adj", None, None, None, None, "tự nhiên, thuộc về tự nhiên", "She likes natural beauty.", None, None),
    ("naturally", "adv", None, None, None, None, "một cách tự nhiên, đương nhiên", "She sings naturally.", None, None),
    ("nature", "noun", None, None, None, None, "thiên nhiên, bản chất", "She loves nature.", None, None),
    ("near", "adv", None, None, None, None, "gần, ở gần", "She lives near the park.", None, None),
    ("nearby", "adv", None, None, None, None, "gần đó, lân cận", "The store is nearby.", None, None),
    ("nearly", "adv", None, None, None, None, "gần như, suýt", "She nearly missed the train.", None, None),
    ("necessarily", "adv", None, None, None, None, "nhất thiết, cần thiết", "It is not necessarily true.", None, None),
    ("necessary", "adj", None, None, None, None, "cần thiết, thiết yếu", "Water is necessary for life.", None, None),
    ("neck", "noun", None, None, None, None, "cổ, cái cổ", "She wore a necklace around her neck.", None, None),
    ("need", "verb", "needed", "needed", "needing", None, "cần, cần thiết", "She needs help.", None, None),
    ("negative", "adj", None, None, None, None, "tiêu cực, phủ định", "The result was negative.", None, None),
    ("negotiate", "verb", "negotiated", "negotiated", "negotiating", None, "đàm phán, thương lượng", "She negotiated the contract.", None, None),
    ("negotiation", "noun", None, None, None, None, "sự đàm phán, thương lượng", "The negotiation was successful.", None, None),
    ("neighbor", "noun", None, None, None, None, "hàng xóm, láng giềng", "Her neighbor is friendly.", None, None),
    ("neighborhood", "noun", None, None, None, None, "khu phố, vùng lân cận", "She lives in a quiet neighborhood.", None, None),
    ("neither", "adv", None, None, None, None, "không, cũng không", "Neither answer is correct.", None, None),
    ("nerve", "noun", None, None, None, None, "dây thần kinh, sự can đảm", "She has strong nerves.", None, None),
    ("nervous", "adj", None, None, None, None, "lo lắng, hồi hộp", "She is nervous before exams.", None, None),
    ("net", "noun", None, None, None, None, "lưới, mạng", "The net is full of fish.", None, None),
    ("network", "noun", None, None, None, None, "mạng lưới, hệ thống", "She joined a business network.", None, None),
    ("never", "adv", None, None, None, None, "không bao giờ, chưa từng", "She never smokes.", None, None),
    ("nevertheless", "adv", None, None, None, None, "tuy nhiên, dù sao", "Nevertheless, she tried.", None, None),
    ("new", "adj", None, None, None, None, "mới, mới mẻ", "She bought a new car.", None, None),
    ("newly", "adv", None, None, None, None, "mới đây, vừa mới", "She is newly married.", None, None),
    ("news", "noun", None, None, None, None, "tin tức, bản tin", "She watches the news.", None, None),
    ("newspaper", "noun", None, None, None, None, "báo, tờ báo", "She reads the newspaper.", None, None),
    ("next", "adj", None, None, None, None, "tiếp theo, kế tiếp", "The next train is at 5.", None, None),
    ("nice", "adj", None, None, None, None, "tốt, đẹp, dễ chịu", "She is a nice person.", None, None),
    ("night", "noun", None, None, None, None, "đêm, buổi tối", "She sleeps at night.", None, None),
    ("nine", "num", None, None, None, None, "chín, số chín", "There are nine apples.", None, None),
    ("no", "adv", None, None, None, None, "không, từ chối", "No, I don't want it.", None, None),
    ("nobody", "pron", None, None, None, None, "không ai, chẳng ai", "Nobody knows the answer.", None, None),
    ("nod", "verb", "nodded", "nodded", "nodding", None, "gật đầu, cúi đầu", "She nodded in agreement.", None, None),
    ("noise", "noun", None, None, None, None, "tiếng ồn, sự ồn ào", "The noise was loud.", None, None),
    ("nomination", "noun", None, None, None, None, "sự đề cử, bổ nhiệm", "She received a nomination.", None, None),
    ("none", "pron", None, None, None, None, "không ai, không cái nào", "None of the answers are correct.", None, None),
    ("nonetheless", "adv", None, None, None, None, "tuy nhiên, dù sao", "Nonetheless, she continued.", None, None),
    ("nor", "conj", None, None, None, None, "cũng không, không phải", "He did not go, nor did she.", None, None),
    ("normal", "adj", None, None, None, None, "bình thường, thông thường", "This is a normal day.", None, None),
    ("normally", "adv", None, None, None, None, "thông thường, bình thường", "She normally wakes up early.", None, None),
    ("north", "noun", None, None, None, None, "phía bắc, hướng bắc", "She lives in the north.", None, None),
    ("northern", "adj", None, None, None, None, "phía bắc, thuộc về phía bắc", "She is from the northern region.", None, None),
    ("nose", "noun", None, None, None, None, "mũi, cái mũi", "She has a small nose.", None, None),
    ("not", "adv", None, None, None, None, "không, chưa", "She is not ready.", None, None),
    ("note", "noun", None, None, None, None, "ghi chú, giấy ghi chú", "She wrote a note.", None, None),
    ("nothing", "pron", None, None, None, None, "không gì, không có gì", "Nothing is impossible.", None, None),
    ("notice", "verb", "noticed", "noticed", "noticing", None, "nhận thấy, chú ý", "She noticed the change.", None, None),
    ("notion", "noun", None, None, None, None, "khái niệm, ý tưởng", "She has a notion about the plan.", None, None),
    ("novel", "noun", None, None, None, None, "tiểu thuyết, mới lạ", "She wrote a novel.", None, None),
    ("now", "adv", None, None, None, None, "bây giờ, hiện tại", "She is working now.", None, None),
    ("nowhere", "adv", None, None, None, None, "không nơi nào, không chỗ nào", "She found it nowhere.", None, None),
    ("n't", "adv", None, None, None, None, "không, viết tắt của not", "She isn't coming.", None, None),
    ("nuclear", "adj", None, None, None, None, "hạt nhân, thuộc về hạt nhân", "She studies nuclear physics.", None, None),
    ("number", "noun", None, None, None, None, "số, con số", "The number is large.", None, None),
    ("numerous", "adj", None, None, None, None, "nhiều, đông đảo", "She has numerous friends.", None, None),
    ("nurse", "noun", None, None, None, None, "y tá, điều dưỡng", "She is a nurse.", None, None),
    ("nut", "noun", None, None, None, None, "hạt, quả hạch", "She ate a nut.", None, None),
    ("object", "noun", None, None, None, None, "vật, đồ vật", "She found a strange object.", None, None),
    ("objective", "noun", None, None, None, None, "mục tiêu, khách quan", "Her objective is clear.", None, None),
    ("obligation", "noun", None, None, None, None, "nghĩa vụ, bổn phận", "She has an obligation to help.", None, None),
    ("observation", "noun", None, None, None, None, "sự quan sát, nhận xét", "Her observation was accurate.", None, None),
    ("observe", "verb", "observed", "observed", "observing", None, "quan sát, theo dõi", "She observed the birds.", None, None),
    ("observer", "noun", None, None, None, None, "người quan sát, giám sát", "He is an observer.", None, None),
    ("obtain", "verb", "obtained", "obtained", "obtaining", None, "đạt được, giành được", "She obtained a degree.", None, None),
    ("obvious", "adj", None, None, None, None, "rõ ràng, hiển nhiên", "The answer is obvious.", None, None),
    ("obviously", "adv", None, None, None, None, "rõ ràng, hiển nhiên", "She is obviously tired.", None, None),
    ("occasion", "noun", None, None, None, None, "dịp, cơ hội", "It was a special occasion.", None, None),
    ("occasionally", "adv", None, None, None, None, "thỉnh thoảng, đôi khi", "She occasionally travels.", None, None),
    ("occupation", "noun", None, None, None, None, "nghề nghiệp, sự chiếm đóng", "Her occupation is teaching.", None, None),
    ("occupy", "verb", "occupied", "occupied", "occupying", None, "chiếm, giữ, ở", "She occupied the seat.", None, None),
    ("occur", "verb", "occurred", "occurred", "occurring", None, "xảy ra, xuất hiện", "The event occurred yesterday.", None, None),
    ("ocean", "noun", None, None, None, None, "đại dương, biển", "She swam in the ocean.", None, None),
    ("odd", "adj", None, None, None, None, "kỳ lạ, lẻ", "The number is odd.", None, None),
    ("odds", "noun", None, None, None, None, "tỷ lệ, cơ hội", "The odds are low.", None, None),
    ("of", "prep", None, None, None, None, "của, thuộc về", "She is a friend of mine.", None, None),
    ("off", "adv", None, None, None, None, "tắt, rời khỏi", "The light is off.", None, None),
    ("offense", "noun", None, None, None, None, "sự xúc phạm, tội lỗi", "He committed an offense.", None, None),
    ("offensive", "adj", None, None, None, None, "xúc phạm, công kích", "His comments were offensive.", None, None),
    ("offer", "verb", "offered", "offered", "offering", None, "đề nghị, cung cấp", "She offered him a job.", None, None),
    ("office", "noun", None, None, None, None, "văn phòng, cơ quan", "She works in an office.", None, None),
    ("officer", "noun", None, None, None, None, "sĩ quan, nhân viên", "He is a police officer.", None, None),
    ("official", "adj", None, None, None, None, "chính thức, thuộc về chính quyền", "This is an official document.", None, None),
    ("often", "adv", None, None, None, None, "thường xuyên", "She often goes to the gym.", None, None),
    ("oh", "interj", None, None, None, None, "ồ, ôi", "Oh, I see!", None, None),
    ("oil", "noun", None, None, None, None, "dầu, dầu mỏ", "The car needs oil.", None, None),
    ("ok", "adv", None, None, None, None, "được, ổn", "Is everything ok?", None, None),
    ("okay", "adv", None, None, None, None, "được, ổn", "Okay, let's go.", None, None),
    ("old", "adj", None, None, None, None, "cũ, già", "He is an old man.", None, None),
    ("Olympic", "adj", None, None, None, None, "thuộc về Olympic", "The Olympic Games are exciting.", None, None),
    ("on", "prep", None, None, None, None, "trên, ở trên", "The book is on the table.", None, None),
    ("once", "adv", None, None, None, None, "một lần, đã từng", "I visited Paris once.", None, None),
    ("one", "num", None, None, None, None, "một, số một", "She has one cat.", None, None),
    ("ongoing", "adj", None, None, None, None, "đang diễn ra", "The project is ongoing.", None, None),
    ("onion", "noun", None, None, None, None, "hành tây", "She chopped an onion.", None, None),
    ("online", "adj", None, None, None, None, "trực tuyến", "The meeting is online.", None, None),
    ("only", "adv", None, None, None, None, "chỉ, duy nhất", "She is the only child.", None, None),
    ("onto", "prep", None, None, None, None, "lên trên", "He climbed onto the roof.", None, None),
    ("open", "verb", "opened", "opened", "opening", None, "mở, khai trương", "She opened the door.", None, None),
    ("opening", "noun", None, None, None, None, "sự mở đầu, khai trương", "The opening ceremony was grand.", None, None),
    ("operate", "verb", "operated", "operated", "operating", None, "vận hành, hoạt động", "She operates the machine.", None, None),
    ("operation", "noun", None, None, None, None, "sự hoạt động, ca mổ", "The operation was successful.", None, None),
    ("operator", "noun", None, None, None, None, "người điều hành, tổng đài viên", "He is a phone operator.", None, None),
    ("opinion", "noun", None, None, None, None, "ý kiến, quan điểm", "She expressed her opinion.", None, None),
    ("opponent", "noun", None, None, None, None, "đối thủ, kẻ thù", "He is a strong opponent.", None, None),
    ("opportunity", "noun", None, None, None, None, "cơ hội, dịp", "She got a great opportunity.", None, None),
    ("oppose", "verb", "opposed", "opposed", "opposing", None, "phản đối, chống lại", "They oppose the plan.", None, None),
    ("opposite", "adj", None, None, None, None, "đối diện, ngược lại", "The bank is opposite the park.", None, None),
    ("option", "noun", None, None, None, None, "lựa chọn, phương án", "She has many options.", None, None),
    ("or", "conj", None, None, None, None, "hoặc, hay là", "Do you want tea or coffee?", None, None),
    ("orange", "noun", None, None, None, None, "quả cam, màu cam", "She ate an orange.", None, None),
    ("order", "noun", None, None, None, None, "đơn hàng, thứ tự", "I would like to place an order.", None, None),
    ("ordinary", "adj", None, None, None, None, "bình thường, thông thường", "It was an ordinary day.", None, None),
    ("organ", "noun", None, None, None, None, "cơ quan nội tạng, đàn organ", "The heart is a vital organ.", None, None),
    ("organization","noun",None,None,None,None,"tổ chức, cơ quan","She works for a non-profit organization.", None, None),
    ("organize","verb","organized","organized","organizing",None,"tổ chức, sắp xếp","She organized the event.", None, None),
    ("orientation","noun",None,None,None,None,"sự định hướng, hướng dẫn","The orientation was helpful.", None, None),
    ("origin","noun",None,None,None,None,"nguồn gốc, xuất xứ","The origin of the word is Latin.", None, None),
    ("original","adj",None,None,None,None,"nguyên bản, độc đáo","The painting is an original work.", None, None),
    ("originally","adv",None,None,None,None,"ban đầu, nguyên gốc","She originally wanted to be a doctor.", None, None),
    ("other","adj",None,None,None,None,"khác, khác nhau","She has two other options.", None, None),
    ("others","pron",None,None,None,None,"những người khác, những cái khác","The others are waiting.", None, None),
    ("otherwise","adv",None,None,None,None,"nếu không thì, mặt khác","You must hurry, otherwise you'll be late.", None, None),
    ("ought","verb","ought to","ought to","oughting",None,"nên, phải","You ought to apologize.", None, None),
    ("our","pron",None,None,None,None,"của chúng tôi, của chúng ta","Our house is big."),
    ("ourselves","pron",None,None,None,None,"chính chúng tôi, tự chúng tôi","We did it ourselves."),
    ("out","adv",None,None,None,None,"ra ngoài, hết","She went out."),
    ("outcome","noun",None,None,None,None,"kết quả, hậu quả","The outcome was positive."),
    ("outside","adv",None,None,None,None,"bên ngoài, ở ngoài","She waited outside."),
    ("oven","noun",None,None,None,None,"lò nướng, lò sưởi","She baked a cake in the oven."),
    ("over","prep",None,None,None,None,"trên, vượt qua","The plane flew over the city."),
    ("overall","adj",None,None,None,None,"tổng thể, toàn bộ","The overall plan is good."),
    ("overcome","verb","overcame","overcome","overcoming",None,"vượt qua, khắc phục","She overcame her fears."),
    ("overlook","verb","overlooked","overlooked","overlooking",None,"bỏ qua, nhìn ra","She overlooked the mistake."),
    ("owe","verb","owed","owed","owing",None,"nợ, mang ơn","She owes me money."),
    ("own","verb","owned","owned","owning",None,"sở hữu, có riêng","She owns a car."),
    ("owner","noun",None,None,None,None,"chủ sở hữu, ông chủ","He is the owner of the business."),
    ("pace","noun",None,None,None,None,"nhịp độ, bước đi","The pace of life is fast."),
    ("pack","verb","packed","packed","packing",None,"đóng gói, xếp hàng","She packed her suitcase."),
    ("package","noun",None,None,None,None,"gói hàng, bưu kiện","She received a package."),
    ("page","noun",None,None,None,None,"trang, trang giấy","She turned the page."),
    ("pain","noun",None,None,None,None,"đau đớn, nỗi đau","She felt pain in her leg."),
    ("painful","adj",None,None,None,None,"đau đớn, đau khổ","The injury was painful."),
    ("paint","verb","painted","painted","painting",None,"sơn, vẽ tranh","She painted a picture."),
    ("painter","noun",None,None,None,None,"họa sĩ, thợ sơn","He is a famous painter."),
    ("painting","noun",None,None,None,None,"bức tranh, sự vẽ tranh","The painting is beautiful."),
    ("pair","noun",None,None,None,None,"cặp, đôi","She bought a new pair of shoes."),
    ("pale","adj",None,None,None,None,"nhợt nhạt, tái nhợt","She looked pale after the illness.","faint","bright"),
 ]



# Xóa file database cũ nếu tồn tại và tạo database mới
try:
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    # Nếu xóa thành công, ta tiếp tục tạo DB mới.
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

except PermissionError:
    print(f"LỖI: Database '{DB_NAME}' đang bị ứng dụng khác khóa. Đang thử kết nối để DROP TABLE.")
    # Nếu xóa thất bại do PermissionError, ta kết nối đến file đang tồn tại và DROP TABLE
    # để tránh lỗi "table already exists"
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Thử xóa bảng nếu nó đã tồn tại
    c.execute("DROP TABLE IF EXISTS words")

# Tạo bảng (luôn chạy, vì nếu xóa được thì là tạo mới, nếu không xóa được thì đã DROP TABLE)
c.execute("""
    CREATE TABLE words (
        word TEXT NOT NULL,
        pronunciation TEXT,
        type TEXT,
        v2 TEXT,
        v3 TEXT,
        ing TEXT,
        ed TEXT,
        meaning TEXT,
        example TEXT,
        synonym TEXT,
        antonym TEXT
    )
""")

# Chèn dữ liệu
total_inserted = 0
for row_10_columns in data:
    # row_10_columns = (word, type, v2, v3, ing, ed, meaning, example, synonym, antonym)
    word = row_10_columns[0]
    
    # Lấy phiên âm (vị trí thứ 2) từ map, nếu không có thì dùng None
    pronunciation = pron_map.get(word, None)
    
    # Tạo hàng dữ liệu 11 cột mới: (word, pronunciation, type, ...)
    final_row = [word, pronunciation] + list(row_10_columns[1:])
    
    if len(final_row) == 11:
        c.execute("""
            INSERT INTO words 
            (word, pronunciation, type, v2, v3, ing, ed, meaning, example, synonym, antonym) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, final_row)
        total_inserted += 1

# Commit các thay đổi và đóng kết nối
conn.commit()
conn.close()

print(f"Đã tạo database '{DB_NAME}' và chèn thành công {total_inserted} từ.")
print("Vui lòng chạy lại ứng dụng Flask (app.py) để tải dữ liệu mới.")
