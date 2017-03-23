# hypnotics = [
# 	'CHLORAL HYDRATE',
# 	'CLOMETHIAZOLE',
# 	'DEXMEDETOMIDINE',
# 	'MELATONIN',
# 	'MEPROBAMATE',
#     'ZALEPLON',
#     'zopiclone',
#     'ZOLPIDEM'
# ]
#
# zdrugs = [
#     'ZALEPLON',
#     'zopiclone',
#     'ZOLPIDEM'
# ]

mood_stabilisers = {
    #my own list:
    'drugs':[
        'carbamazepine',
        'gabapentin',
        'LAMOTRIGINE',
        'PREGABALIN',
        'SODIUM VALPROATE',
        'VALPROIC ACID',
        'lithium citrate',
        'lithium carbonate',
        'Valproate semisodium'
        ],
    'depot':False,
    'name':'mood_stabilisers'
}

sedatives = {
    'drugs':[
        # BNF benzodiazepines:
    	'ALPRAZOLAM',
    	'CHLORDIAZEPOXIDE HYDROCHLORIDE',
    	'CLOBAZAM',
    	'CLONAZEPAM',
    	'FLURAZEPAM',
        'Flurazepam hydrochloride',
    	'LOPRAZOLAM',
    	'LORAZEPAM',
    	'LORMETAZEPAM',
    	'MIDAZOLAM',
        'Midazolam Hydrochloride',
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
        'zolpidem tartrate',
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
    	'HYDROXYZINE HYDROCHLORIDE',
    	'KETOTIFEN',
    	'MORPHINE WITH CYCLIZINE',
    	'PARACETAMOL WITH BUCLIZINE HYDROCHLORIDE AND CODEINE PHOSPHATE',
        'Buclizine hydrochloride/Paracetamol/Codeine phosphate',
    	'PIZOTIFEN',
    	'PROMETHAZINE TEOCLATE',
        'PROMETHAZINE hydrochloride',
        #My own additions
    	'CHLORDIAZEPOXIDE'
        ],
    'depot':False,
    'name':'sedatives'
}

fgas = {
    'drugs':[
    #from BNF 2017:
    'AMITRIPTYLINE WITH PERPHENAZINE',
    'BENPERIDOL',
    'CHLORPROMAZINE HYDROCHLORIDE',
    'DROPERIDOL',
    'FLUPENTIXOL',
    'HALOPERIDOL',
    'LEVOMEPROMAZINE',
    'PERICYAZINE',
    'PERPHENAZINE',
    'PIMOZIDE',
    'PROCHLORPERAZINE',
    'PROMAZINE HYDROCHLORIDE',
    'SULPIRIDE',
    'TRIFLUOPERAZINE',
    'ZUCLOPENTHIXOL',
    'ZUCLOPENTHIXOL ACETATE',
    #My own additions
    'Trifluoperazine hydrochloride',
    'Prochlorperazine maleate',
    'Prochlorperazine mesilate',
    'Zuclopenthixol dihydrochloride'
    ],
    'depot':False,
    'name':'sedatives'
}
sgas = {
    'drugs':[
    #from BNF 2017:
    'AMISULPRIDE',
    'ARIPIPRAZOLE',
    'ASENAPINE',
    'CLOZAPINE',
    'LURASIDONE HYDROCHLORIDE',
    'OLANZAPINE',
    'PALIPERIDONE',
    'QUETIAPINE',
    'RISPERIDONE'
    ],
    'depot':False,
    'name':'sgas'
}

fga_depots = {
    'drugs':[
    #from BNF 2017:
    'FLUPENTIXOL DECANOATE',
    'FLUPHENAZINE DECANOATE',
    'HALOPERIDOL DECANOATE',
    'ZUCLOPENTHIXOL DECANOATE',
    #My own additions:
    ],
    'depot':True,
    'name':'fga_depots'
}

sga_depots = {
    'drugs':[
    #from BNF 2017:
    'ARIPIPRAZOLE',
    'OLANZAPINE EMBONATE',
    'PALIPERIDONE',
    'RISPERIDONE',
    #My own additions:
    'Olanzapine embonate monohydrate'
    ],
    'depot':True,
    'name':'sga_depots'
}

antidepressants = {
    'drugs':[
    #from BNF 2017:
    'VORTIOXETINE',
    'MIANSERIN HYDROCHLORIDE',
    'MIRTAZAPINE',
    'AMITRIPTYLINE HYDROCHLORIDE',
    'AMITRIPTYLINE WITH PERPHENAZINE',
    'CLOMIPRAMINE HYDROCHLORIDE',
    'DOSULEPIN HYDROCHLORIDE',
    'DOXEPIN',
    'IMIPRAMINE HYDROCHLORIDE',
    'LOFEPRAMINE',
    'NORTRIPTYLINE',
    'TRIMIPRAMINE',
    'CITALOPRAM',
    'DAPOXETINE',
    'ESCITALOPRAM',
    'FLUOXETINE',
    'FLUVOXAMINE MALEATE',
    'PAROXETINE',
    'SERTRALINE',
    'BUPROPION HYDROCHLORIDE',
    'DULOXETINE',
    'VENLAFAXINE',
    'BUSPIRONE HYDROCHLORIDE',
    'TRAZODONE HYDROCHLORIDE',
    'REBOXETINE',
    #My own list:
    'Citalopram hydrobromide',
    'Citalopram hydrochloride',
    'Dosulepin Hydrochloride',
    'Doxepin hydrochloride',
    'Duloxetine hydrochloride',
    'Escitalopram oxalate',
    'Fluoxetine hydrochloride',
    'Fluvoxamine maleate',
    'Lofepramine hydrochloride',
    'Mianserin',
    'Nortriptyline hydrochloride',
    'Paroxetine hydrochloride',
    'Reboxetine mesilate',
    'Sertraline hydrochloride',
    'Trimipramine maleate',
    'Trimipramine maleate',
    'Venlafaxine Hydrochloride'],
    'depot':False,
    'name':'antidepressants'
}

antidementia_drugs = [
    'DONEPEZIL HYDROCHLORIDE',
    'GALANTAMINE',
    'RIVASTIGMINE',
    'Memantine hydrochloride',
    'memantine',
    'donepezil'
]
