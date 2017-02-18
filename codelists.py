hypnotics = [
	'CHLORAL HYDRATE',
	'CLOMETHIAZOLE',
	'DEXMEDETOMIDINE',
	'MELATONIN',
	'MEPROBAMATE',
    'ZALEPLON',
    'zopiclone',
    'ZOLPIDEM'
]

zdrugs = [
    'ZALEPLON',
    'zopiclone',
    'ZOLPIDEM'
]

sedatives = [
    # BNF benzodiazepines:
	'ALPRAZOLAM',
	'CHLORDIAZEPOXIDE HYDROCHLORIDE',
	'CLOBAZAM',
	'CLONAZEPAM',
	'FLURAZEPAM',
	'LOPRAZOLAM',
	'LORAZEPAM',
	'LORMETAZEPAM',
	'MIDAZOLAM',
	'NITRAZEPAM',
	'OXAZEPAM',
	'TEMAZEPAM',
    # BNF Non-benzodiazepine hypnotics and sedatives
	'CHLORAL HYDRATE',
	'CLOMETHIAZOLE',
	'DEXMEDETOMIDINE',
	'MELATONIN',
	'MEPROBAMATE',
    'ZALEPLON',
    'zopiclone',
    'ZOLPIDEM',
    #BNF sedating antihistamines
	'ALIMEMAZINE TARTRATE',
	'ANTAZOLINE WITH XYLOMETAZOLINE',
	'CHLORPHENAMINE MALEATE',
	'CINNARIZINE',
	'CINNARIZINE WITH DIMENHYDRINATE',
	'CLEMASTINE',
	'CYPROHEPTADINE HYDROCHLORIDE',
	'ERGOTAMINE TARTRATE WITH CAFFEINE HYDRATE AND CYCLIZINE HYDROCHLORIDE',
	'HYDROXYZINE HYDROXYZINE HYDROCHLORIDE',
	'KETOTIFEN',
	'MORPHINE WITH CYCLIZINE',
	'PARACETAMOL WITH BUCLIZINE HYDROCHLORIDE AND CODEINE PHOSPHATE',
	'PIZOTIFEN',
	'PROMETHAZINE TEOCLATE',
    #My own additions
	'CHLORDIAZEPOXIDE'
]

antidementia_drugs = [
    'donepezil',
    'rivastigmine',
    'memantine',
    'galantamine'
]

insomnia_codes = [
    'R005200', # [D]Insomnia NOS
    '1B1B.11', # C/O - insomnia
    'E274111', # Insomnia NOS
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
    '1BX9.00'  # Light sleep
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
	'129B.00',	#	FH: Alzheimer's disease
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
	'1281.00',	#	FH: Senile dementia
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
