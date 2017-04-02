insomnia_readcodes = [
    'R005200', # [D]Insomnia NOS
    '1B1B.11', # C/O - insomnia
    'R005.00', # [D]Sleep disturbances
    'E274111', # Insomnia NOS
    'Fy00.00',  # Disorders of maintaining and initiating sleep
    '1B1B.00', # Cannot sleep - insomnia
    '663N.00', # Asthma disturbing sleep
    'R005.11', # [D]Insomnia - symptom
    '663N200', # Asthma disturbs sleep frequently
    '663N100', # Asthma disturbs sleep weekly
    'E274100', # Transient insomnia
    '1B1B200', # Late insomnia
    '1B1B000', # Initial insomnia
    'Eu51000', # [X]Nonorganic insomnia
    '1BX0.00', # Delayed onset of sleep
    'E274200', # Persistent insomnia
    '1B1B100', # Middle insomnia
    'E274D11', # Restless sleep
    'E274.12', # Insomnia due to nonorganic sleep disorder
    'E274E00', # 'Short-sleeper'
    '1BX9.00', # Light sleep
    '1B1Q.00' # Poor sleep pattern

]

dementia_readcodes = [
	'E001000',	#	Uncomplicated presenile dementia
	'E001z00',	#	Presenile dementia NOS
	'E002.00',	#	Senile dementia with depressive or paranoid fe...
	'Eu00012',	#	[X]Primary degen dementia, Alzheimer's type, p...
	'Eu00013',	#	[X]Alzheimer's disease type 2
	'Eu00011',	#	[X]Presenile dementia,Alzheimer's type
	'Eu02400',	#	[X]Dementia in human immunodef virus [HIV] dis...
	'Eu02z00',	#	[X] Unspecified dementia
	'E004000',	#	Uncomplicated arteriosclerotic dementia
	'Eu10711',	#	[X]Alcoholic dementia NOS
	'Eu01100',	#	[X]Multi-infarct dementia
	'E001.00',	#	Presenile dementia
	'E001100',	#	Presenile dementia with delirium
	'Eu01.00',	#	[X]Vascular dementia
	'E002z00',	#	Senile dementia with depressive or paranoid fe...
	'E004100',	#	Arteriosclerotic dementia with delirium
	'E02y100',	#	Drug-induced dementia
	'Eu02500',	#	[X]Lewy body dementia
	'Eu00000',	#	[X]Dementia in Alzheimer's disease with early ...
	'E004300',	#	Arteriosclerotic dementia with depression
	'E003.00',	#	Senile dementia with delirium
	'Eu00112',	#	[X]Senile dementia,Alzheimer's type
	'E004.00',	#	Arteriosclerotic dementia
	'E004200',	#	Arteriosclerotic dementia with paranoia
	'E000.00',	#	Uncomplicated senile dementia
	'Eu00100',	#	[X]Dementia in Alzheimer's disease with late o...
	'E004z00',	#	Arteriosclerotic dementia NOS
	'Eu01.11',	#	[X]Arteriosclerotic dementia
	'Eu02300',	#	[X]Dementia in Parkinson's disease
	'Eu01000',	#	[X]Vascular dementia of acute onset
	'F116.00',	#	Lewy body disease
	'Eu00.00',	#	[X]Dementia in Alzheimer's disease
	'E004.11',	#	Multi infarct dementia
	'Eu02000',	#	[X]Dementia in Pick's disease
	'Eu00113',	#	[X]Primary degen dementia of Alzheimer's type,...
	'Eu00111',	#	[X]Alzheimer's disease type 1
	'E00..11',	#	Senile dementia
	'Eu01300',	#	[X]Mixed cortical and subcortical vascular dem...
	'Eu01y00',	#	[X]Other vascular dementia
	'Eu04100',	#	[X]Delirium superimposed on dementia
	'Eu02z11',	#	[X] Presenile dementia NOS
	'Eu02z16',	#	[X] Senile dementia, depressed or paranoid type
	'Eu02z14',	#	[X] Senile dementia NOS
	'E002100',	#	Senile dementia with depression
	'Eu02100',	#	[X]Dementia in Creutzfeldt-Jakob disease
	'1461.00',	#	H/O: dementia
	'Eu01111',	#	[X]Predominantly cortical dementia
	'E001200',	#	Presenile dementia with paranoia
	'Eu02z13',	#	[X] Primary degenerative dementia NOS
	'F110000',	#	Alzheimer's disease with early onset
	'F111.00',	#	Pick's disease
	'Eu02.00',	#	[X]Dementia in other diseases classified elsew...
	'Eu01200',	#	[X]Subcortical vascular dementia
	'ZS7C500',	#	Language disorder of dementia
	'E00..12',	#	Senile/presenile dementia
	'E002000',	#	Senile dementia with paranoia
	'Eu00z11',	#	[X]Alzheimer's dementia unspec
	'E012.11',	#	Alcoholic dementia NOS
	'Eu02200',	#	[X]Dementia in Huntington's disease
	'E012.00',	#	Other alcoholic dementia
	'E001300',	#	Presenile dementia with depression
	'F110100',	#	Alzheimer's disease with late onset
	'F112.00',	#	Senile degeneration of brain
	'F110.00',	#	Alzheimer's disease
	'Eu02y00',	#	[X]Dementia in other specified diseases classi...
	'Eu00200',	#	[X]Dementia in Alzheimer's dis, atypical or mi...
	'Fyu3000',	#	[X]Other Alzheimer's disease
	'Eu00z00',	#	[X]Dementia in Alzheimer's disease, unspecified
	'Eu01z00'	#	[X]Vascular dementia, unspecified
]

clin_sig_alcohol_use = {
    'name': 'clin_sig_alcohol_use',
    'codes': [
    	'1366',		    #Very heavy drinker - >9u/day
    	'136Q.00',		#Very heavy drinker
    	'136T.00',		#harmful alcohol use
    	'1462',		    #h/o: alcoholism
    	'1B1c.00',		#alcohol induced hallucinations
    	'66e0.00',		#alcohol abuse monitoring
    	'7P22100',		#delivery of rehabilitation for alcohol addiction
    	'8BA8.00',		#alcohol detoxification
    	'8CAv.00',		#advised to contact primary care alcohol worker
    	'8G32.00',		#aversion therapy - alcoholism
    	'8H35.00',		#admitted to alcohol detoxification centre
    	'8HkG.00',		#referral to specialist alcohol treatment service
    	'8IAF.00',		#brief intervention for excessive alcohol consumptn declined
    	'8IAJ.00',		#declined referral to specialist alcohol treatment service
    	'8IAt.00',		#extended interven for excessive alcohol consumption declined
    	'9k1B.00',		#extended intervention for excessive alcohol consumptn complt
    	'9NN2.00',		#under care of community alcohol team
    	'C150500',		#alcohol-induced pseudo-cushing's syndrome
    	'E01..00',		#alcoholic psychoses
    	'E010.00',		#alcohol withdrawal delirium
    	'E011000',		#korsakov's alcoholic psychosis
    	'E011100',		#korsakov's alcoholic psychosis with peripheral neuritis
    	'E011200',		#Wernicke-Korsakov syndrome
    	'E011z00',		#alcohol amnestic syndrome nos
    	'E012.00',		#other alcoholic dementia
    	'E012000',		#chronic alcoholic brain syndrome
    	'E012.11',		#alcoholic dementia nos
    	'E013.00',		#alcohol withdrawal hallucinosis
    	'E014.00',		#pathological alcohol intoxication
    	'E015.00',		#alcoholic paranoia
    	'E01y.00',		#other alcoholic psychosis
    	'E01y000',		#alcohol withdrawal syndrome
    	'E01yz00',		#other alcoholic psychosis nos
    	'E01z.00',		#alcoholic psychosis nos
    	'E23..00',		#alcohol dependence syndrome
    	'E230.00',		#acute alcoholic intoxication in alcoholism
    	'E230000',		#acute alcoholic intoxication; unspecified; in alcoholism
    	'E230100',		#continuous acute alcoholic intoxication in alcoholism
    	'E230.11',		#alcohol dependence with acute alcoholic intoxication
    	'E230200',		#episodic acute alcoholic intoxication in alcoholism
    	'E230300',		#acute alcoholic intoxication in remission; in alcoholism
    	'E230z00',		#acute alcoholic intoxication in alcoholism nos
    	'E231.00',		#chronic alcoholism
    	'E231000',		#unspecified chronic alcoholism
    	'E23..11',		#alcoholism
    	'E231100',		#continuous chronic alcoholism
    	'E231200',		#episodic chronic alcoholism
    	'E231300',		#chronic alcoholism in remission
    	'E231z00',		#chronic alcoholism nos
    	'E23z.00',		#alcohol dependence syndrome nos
    	'E250300',		#nondependent alcohol abuse in remission
    	'Eu10.00',		#[x]mental and behavioural disorders due to use of alcohol
    	'Eu10100',		#[x]mental and behav dis due to use of alcohol: harmful use
    	'Eu10200',		#[x]mental and behav dis due to use alcohol: dependence syndr
    	'Eu10211',		#[x]alcohol addiction
    	'Eu10212',		#[x]chronic alcoholism
    	'Eu10300',		#[x]mental and behav dis due to use alcohol: withdrawal state
    	'Eu10400',		#[X]Men & behav dis due alcohl: withdrawl state with delirium
    	'Eu10411',		#[x]delirium tremens; alcohol induced
    	'Eu10500',		#[x]mental & behav dis due to use alcohol: psychotic disorder
    	'Eu10511',		#[x]alcoholic hallucinosis
    	'Eu10512',		#[x]alcoholic jealousy
    	'Eu10513',		#[x]alcoholic paranoia
    	'Eu10514',		#[x]alcoholic psychosis nos
    	'Eu10600',		#[x]mental and behav dis due to use alcohol: amnesic syndrome
    	'Eu10611',		#[x]korsakov's psychosis; alcohol induced
    	'Eu10700',		#[X]Men & behav dis due alcoh: resid & late-onset psychot dis
    	'Eu10711',		#[x]alcoholic dementia nos
    	'Eu10712',		#[x]chronic alcoholic brain syndrome
    	'Eu10800',		#[x]alcohol withdrawal-induced seizure
    	'Eu10y00',		#[x]men & behav dis due to use alcohol: oth men & behav dis
    	'Eu10z00',		#[x]ment & behav dis due use alcohol: unsp ment & behav dis
    	'F11x000',		#cerebral degeneration due to alcoholism
    	'F11x011',		#alcoholic encephalopathy
    	'F144000',		#cerebellar ataxia due to alcoholism
    	'F25B.00',		#alcohol-induced epilepsy
    	'F375.00',		#alcoholic polyneuropathy
    	'F394100',		#alcoholic myopathy
    	'G555.00',		#alcoholic cardiomyopathy
    	'G852300',		#oesophageal varices in alcoholic cirrhosis of the liver
    	'J610.00',		#alcoholic fatty liver
    	'J611.00',		#acute alcoholic hepatitis
    	'J612.00',		#alcoholic cirrhosis of liver
    	'J612000',		#alcoholic fibrosis and sclerosis of liver
    	'J613.00',		#alcoholic liver damage unspecified
    	'J613000',		#alcoholic hepatic failure
    	'J617.00',		#alcoholic hepatitis
    	'J617000',		#chronic alcoholic hepatitis
    	'J671000',		#alcohol-induced chronic pancreatitis
    	'SLH3.00',		#alcohol deterrent poisoning
    	'SM00100',		#denatured alcohol causing toxic effect
    	'U60H300',		#[x]alcohol deterrents caus adverse effects in therapeut use
    	'U60H311',		#[x] adverse reaction to alcohol deterrents
    	'Z191.00',		#alcohol detoxification
    	'Z191100',		#alcohol withdrawal regime
    	'Z191211',		#alcohol reduction programme
    	'ZR1E.11',		#ads - alcohol dependence scale
    	'ZV11300'		#[v]personal history of alcoholism
        ]
}
