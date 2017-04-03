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

mental_illness_non_smi = {
    'name': '',
    'codes':[
        #taken from https://clinicalcodes.rss.mhs.man.ac.uk/medcodes/article/38/

        # anxiety disorder
    	'2258',		#O/E - anxious
    	'225J.00',		#O/E - panic attack
    	'8G52.00',		#Antiphobic therapy
    	'8G94.00',		#Anxiety management training
    	'8HHp.00',		#Referral for guided self-help for anxiety
    	'E2...00',		#Neurotic; personality and other nonpsychotic disorders
    	'E20..00',		#Neurotic disorders
    	'E200.00',		#Anxiety states
    	'E200000',		#Anxiety state unspecified
    	'E200100',		#Panic disorder
    	'E200111',		#Panic attack
    	'E200200',		#Generalised anxiety disorder
    	'E200300',		#Anxiety with depression
    	'E200400',		#Chronic anxiety
    	'E200500',		#Recurrent anxiety
    	'E200z00',		#Anxiety state NOS
    	'E201.00',		#Hysteria
    	'E201000',		#Hysteria unspecified
    	'E201100',		#Hysterical blindness
    	'E201200',		#Hysterical deafness
    	'E201300',		#Hysterical tremor
    	'E201400',		#Hysterical paralysis
    	'E201500',		#Hysterical seizures
    	'E201511',		#Fit - hysterical
    	'E201600',		#Other conversion disorder
    	'E201611',		#Astasia - abasia; hysterical
    	'E201612',		#Globus hystericus
    	'E201700',		#Hysterical amnesia
    	'E201800',		#Hysterical fugue
    	'E201900',		#Multiple personality
    	'E201A00',		#Dissociative reaction unspecified
    	'E201B00',		#Compensation neurosis
    	'E201C00',		#Phantom pregnancy
    	'E201z00',		#Hysteria NOS
    	'E201z11',		#Aphonia - hysterical
    	'E201z12',		#Ataxia - hysterical
    	'E201z13',		#Ganser's syndrome - hysterical
    	'E202.00',		#Phobic disorders
    	'E202000',		#Phobia unspecified
    	'E202100',		#Agoraphobia with panic attacks
    	'E202.11',		#Social phobic disorders
    	'E202.12',		#Phobic anxiety
    	'E202200',		#Agoraphobia without mention of panic attacks
    	'E202300',		#Social phobia; fear of eating in public
    	'E202400',		#Social phobia; fear of public speaking
    	'E202500',		#Social phobia; fear of public washing
    	'E202600',		#Acrophobia
    	'E202700',		#Animal phobia
    	'E202800',		#Claustrophobia
    	'E202900',		#Fear of crowds
    	'E202A00',		#Fear of flying
    	'E202B00',		#Cancer phobia
    	'E202C00',		#Dental phobia
    	'E202D00',		#Fear of death
    	'E202E00',		#Fear of pregnancy
    	'E202z00',		#Phobic disorder NOS
    	'E202z11',		#Weight fixation
    	'E203.00',		#Obsessive-compulsive disorders
    	'E203000',		#Compulsive neurosis
    	'E203100',		#Obsessional neurosis
    	'E203.11',		#Anancastic neurosis
    	'E203z00',		#Obsessive-compulsive disorder NOS
    	'E205.00',		#Neurasthenia - nervous debility
    	'E205.11',		#Nervous exhaustion
    	'E205.12',		#Tired all the time
    	'E206.00',		#Depersonalisation syndrome
    	'E207.00',		#Hypochondriasis
    	'E20y.00',		#Other neurotic disorders
    	'E20y000',		#Somatization disorder
    	'E20y011',		#Briquet's disorder
    	'E20y100',		#Writer's cramp neurosis
    	'E20y200',		#Other occupational neurosis
    	'E20y300',		#Psychasthenic neurosis
    	'E20yz00',		#Other neurotic disorder NOS
    	'E20z.00',		#Neurotic disorder NOS
    	'E20z.11',		#Nervous breakdown
    	'E26..00',		#Physiological malfunction arising from mental factors
    	'E260.00',		#Psychogenic musculoskeletal symptoms
    	'E260000',		#Psychogenic paralysis
    	'E260100',		#Psychogenic torticollis
    	'E260z00',		#Psychogenic musculoskeletal symptoms NOS
    	'E261.00',		#Psychogenic respiratory symptoms
    	'E261000',		#Psychogenic air hunger
    	'E261100',		#Psychogenic cough
    	'E261200',		#Psychogenic hiccough
    	'E261300',		#Psychogenic hyperventilation
    	'E261400',		#Psychogenic yawning
    	'E261500',		#Psychogenic aphonia
    	'E261z00',		#Psychogenic respiratory symptom NOS
    	'E262.00',		#Psychogenic cardiovascular symptoms
    	'E262000',		#Cardiac neurosis
    	'E262200',		#Neurocirculatory asthenia
    	'E262300',		#Psychogenic cardiovascular disorder
    	'E262z00',		#Psychogenic cardiovascular symptom NOS
    	'E263.00',		#Psychogenic skin symptoms
    	'E263000',		#Psychogenic pruritus
    	'E263z00',		#Psychogenic skin symptoms NOS
    	'E264.00',		#Psychogenic gastrointestinal tract symptoms
    	'E264000',		#Psychogenic aerophagy
    	'E264011',		#Air swallowing - excessive
    	'E264.11',		#Globus abdominalis
    	'E264200',		#Cyclical vomiting - psychogenic
    	'E264300',		#Psychogenic diarrhoea
    	'E264311',		#Spurious diarrhoea
    	'E264400',		#Psychogenic dyspepsia
    	'E264500',		#Psychogenic constipation
    	'E264z00',		#Psychogenic gastrointestinal tract symptom NOS
    	'E265.00',		#Psychogenic genitourinary tract symptoms
    	'E265100',		#Psychogenic vaginismus
    	'E265200',		#Psychogenic dysmenorrhea
    	'E265300',		#Psychogenic dysuria
    	'E265z00',		#Psychogenic genitourinary tract symptom NOS
    	'E267.00',		#Psychogenic symptom of special sense organ
    	'E26y.00',		#Other psychogenic malfunction
    	'E26y000',		#Bruxism (teeth grinding)
    	'E26yz00',		#Other psychogenic malfunction NOS
    	'E26z.00',		#Psychosomatic disorder NOS
    	'E278.00',		#Psychalgia
    	'E278000',		#Psychogenic pain unspecified
    	'E278100',		#Tension headache
    	'E278111',		#Muscular headache
    	'E278200',		#Psychogenic backache
    	'E278z00',		#Psychalgia NOS
    	'E28..00',		#Acute reaction to stress
    	'E280.00',		#Acute panic state due to acute stress reaction
    	'E281.00',		#Acute fugue state due to acute stress reaction
    	'E28..11',		#Combat fatigue
    	'E282.00',		#Acute stupor state due to acute stress reaction
    	'E283.00',		#Other acute stress reactions
    	'E283000',		#Acute situational disturbance
    	'E283100',		#Acute posttrauma stress state
    	'E283z00',		#Other acute stress reaction NOS
    	'E284.00',		#Stress reaction causing mixed disturbance of emotion/conduct
    	'E28z.00',		#Acute stress reaction NOS
    	'E28z.11',		#Examination fear
    	'E28z.12',		#Flying phobia
    	'E28z.13',		#Stage fright
    	'E29..00',		#Adjustment reaction
    	'E290000',		#Grief reaction
    	'E290011',		#Bereavement reaction
    	'E292.00',		#Adjustment reaction; predominant disturbance other emotions
    	'E292000',		#Separation anxiety disorder
    	'E292100',		#Adolescent emancipation disorder
    	'E292200',		#Early adult emancipation disorder
    	'E292300',		#Specific academic or work inhibition
    	'E292311',		#Specific academic or work inhibition
    	'E292312',		#Specific work inhibition
    	'E292400',		#Adjustment reaction with anxious mood
    	'E292500',		#Culture shock
    	'E292y00',		#Adjustment reaction with mixed disturbance of emotion
    	'E292z00',		#Adjustment reaction with disturbance of other emotion NOS
    	'E293.00',		#Adjustment reaction with predominant disturbance of conduct
    	'E293000',		#Adjustment reaction with aggression
    	'E293100',		#Adjustment reaction with antisocial behaviour
    	'E293200',		#Adjustment reaction with destructiveness
    	'E294.00',		#Adjustment reaction with disturbance emotion and conduct
    	'E29y.00',		#Other adjustment reactions
    	'E29y000',		#Concentration camp syndrome
    	'E29y100',		#Other post-traumatic stress disorder
    	'E29y200',		#Adjustment reaction with physical symptoms
    	'E29y300',		#Elective mutism due to an adjustment reaction
    	'E29y400',		#Adjustment reaction due to hospitalisation
    	'E29y500',		#Other adjustment reaction with withdrawal
    	'E29yz00',		#Other adjustment reactions NOS
    	'E29z.00',		#Adjustment reaction NOS
    	'E2y..00',		#Other specified neuroses or other mental disorders
    	'E2z..00',		#Neuroses or other mental disorder NOS
    	'Eu05400',		#[X]Organic anxiety disorder
    	'Eu34114',		#[X]Persistant anxiety depression
    	'Eu4..00',		#[X]Neurotic; stress - related and somoform disorders
    	'Eu40.00',		#[X]Phobic anxiety disorders
    	'Eu40000',		#[X]Agoraphobia
    	'Eu40011',		#[X]Agoraphobia without history of panic disorder
    	'Eu40012',		#[X]Panic disorder with agoraphobia
    	'Eu40100',		#[X]Social phobias
    	'Eu40112',		#[X]Social neurosis
    	'Eu40200',		#[X]Specific (isolated) phobias
    	'Eu40211',		#[X]Acrophobia
    	'Eu40212',		#[X]Animal phobias
    	'Eu40213',		#[X]Claustrophobia
    	'Eu40214',		#[X]Simple phobia
    	'Eu40300',		#[X]Needle phobia
    	'Eu40y00',		#[X]Other phobic anxiety disorders
    	'Eu40z00',		#[X]Phobic anxiety disorder; unspecified
    	'Eu40z11',		#[X]Phobia NOS
    	'Eu40z12',		#[X]Phobic state NOS
    	'Eu41.00',		#[X]Other anxiety disorders
    	'Eu41000',		#[X]Panic disorder [episodic paroxysmal anxiety]
    	'Eu41011',		#[X]Panic attack
    	'Eu41012',		#[X]Panic state
    	'Eu41100',		#[X]Generalized anxiety disorder
    	'Eu41111',		#[X]Anxiety neurosis
    	'Eu41112',		#[X]Anxiety reaction
    	'Eu41113',		#[X]Anxiety state
    	'Eu41200',		#[X]Mixed anxiety and depressive disorder
    	'Eu41211',		#[X]Mild anxiety depression
    	'Eu41300',		#[X]Other mixed anxiety disorders
    	'Eu41y00',		#[X]Other specified anxiety disorders
    	'Eu41y11',		#[X]Anxiety hysteria
    	'Eu41z00',		#[X]Anxiety disorder; unspecified
    	'Eu41z11',		#[X]Anxiety NOS
    	'Eu42.00',		#[X]Obsessive - compulsive disorder
    	'Eu42000',		#[X]Predominantly obsessional thoughts or ruminations
    	'Eu42100',		#[X]Predominantly compulsive acts [obsessional rituals]
    	'Eu42.11',		#[X]Anankastic neurosis
    	'Eu42.12',		#[X]Obsessive-compulsive neurosis
    	'Eu42200',		#[X]Mixed obsessional thoughts and acts
    	'Eu42y00',		#[X]Other obsessive-compulsive disorders
    	'Eu42z00',		#[X]Obsessive-compulsive disorder; unspecified
    	'Eu43.00',		#[X]Reaction to severe stress; and adjustment disorders
    	'Eu43000',		#[X]Acute stress reaction
    	'Eu43011',		#[X]Acute crisis reaction
    	'Eu43012',		#[X]Acute reaction to stress
    	'Eu43013',		#[X]Combat fatigue
    	'Eu43014',		#[X]Crisis state
    	'Eu43015',		#[X]Psychic shock
    	'Eu43100',		#[X]Post - traumatic stress disorder
    	'Eu43111',		#[X]Traumatic neurosis
    	'Eu43200',		#[X]Adjustment disorders
    	'Eu43211',		#[X]Culture shock
    	'Eu43212',		#[X]Grief reaction
    	'Eu43213',		#[X]Hospitalism in children
    	'Eu43300',		#[X]Acute post-traumatic stress disorder follow military comb
    	'Eu43400',		#[X]Chron post-traumatic stress disorder follow military comb
    	'Eu43y00',		#[X]Other reactions to severe stress
    	'Eu43z00',		#[X]Reaction to severe stress; unspecified
    	'Eu44.00',		#[X]Dissociative [conversion] disorders
    	'Eu44000',		#[X]Dissociative amnesia
    	'Eu44100',		#[X]Dissociative fugue
    	'Eu44.11',		#[X]Conversion hysteria
    	'Eu44.12',		#[X]Conversion reaction
    	'Eu44.13',		#[X]Hysteria
    	'Eu44200',		#[X]Dissociative stupor
    	'Eu44300',		#[X]Trance and possession disorders
    	'Eu44400',		#[X]Dissociative motor disorders
    	'Eu44411',		#[X]Psychogenic aphonia
    	'Eu44412',		#[X]Psychogenic dysphonia
    	'Eu44500',		#[X]Dissociative convulsions
    	'Eu44511',		#[X]Pseudoseizures
    	'Eu44600',		#[X]Dissociative anaesthesia and sensory loss
    	'Eu44611',		#[X]Psychogenic deafness
    	'Eu44700',		#[X]Mixed dissociative [conversion] disorders
    	'Eu44y00',		#[X]Other dissociative [conversion] disorders
    	'Eu44y11',		#[X]Ganser's syndrome
    	'Eu44y12',		#[X]Multiple personality
    	'Eu44y13',		#[X]Psychogenic confusion
    	'Eu44y14',		#[X]Psychogenic twilight state
    	'Eu44z00',		#[X]Dissociative [conversion] disorder; unspecified
    	'Eu45.00',		#[X]Somatoform disorders
    	'Eu45000',		#[X]Somatization disorder
    	'Eu45011',		#[X]Multiple psychosomatic disorder
    	'Eu45012',		#[X]Briquet's syndrome
    	'Eu45100',		#[X]Undifferentiated somatoform disorder
    	'Eu45111',		#[X]Undifferentiated psychosomatic disorder
    	'Eu45200',		#[X]Hypochondriacal disorder
    	'Eu45211',		#[X]Body dysmorphic disorder
    	'Eu45212',		#[X]Dysmorphophobia nondelusional
    	'Eu45213',		#[X]Hypochondriacal neurosis
    	'Eu45214',		#[X]Hypochondriasis
    	'Eu45215',		#[X]Nosophobia
    	'Eu45300',		#[X]Somatoform autonomic dysfunction
    	'Eu45311',		#[X]Cardiac neurosis
    	'Eu45312',		#[X]Da Costa's syndrome
    	'Eu45313',		#[X]Gastric neurosis
    	'Eu45314',		#[X]Neurocirculatory asthenia
    	'Eu45316',		#[X]Psychogenic cough
    	'Eu45317',		#[X]Psychogenic diarrhoea
    	'Eu45318',		#[X]Psychogenic dyspepsia
    	'Eu45319',		#[X]Psychogenic dysuria
    	'Eu45320',		#[X]Psychogenic flatulence
    	'Eu45321',		#[X]Psychogenic hiccough
    	'Eu45322',		#[X]Psychogenic hyperventilat
    	'Eu45323',		#[X]Psychogenic freq micturit
    	'Eu45324',		#[X]Psychogenic IBS
    	'Eu45325',		#[X]Psychogenic pylorospasm
    	'Eu45400',		#[X]Persistent somatoform pain disorder
    	'Eu45411',		#[X]Psychalgia
    	'Eu45412',		#[X]Psychogenic backache
    	'Eu45413',		#[X]Psychogenic headache
    	'Eu45414',		#[X]Somatoform pain disorder
    	'Eu45500',		#[X]Globus pharyngeus
    	'Eu45511',		#[X]Globus hystericus
    	'Eu45y00',		#[X]Other somatoform disorders
    	'Eu45y11',		#[X]Psychogenic dysmenorrhoea
    	'Eu45y12',		#[X]Globus hystericus
    	'Eu45y13',		#[X]Psychogenic pruritis
    	'Eu45y14',		#[X]Psychogenic torticollis
    	'Eu45y15',		#[X]Teeth-grinding
    	'Eu45z00',		#[X]Somatoform disorder; unspecified
    	'Eu45z11',		#[X]Psychosomatic disorder NOS
    	'Eu46.00',		#[X]Other neurotic disorders
    	'Eu46000',		#[X]Neurasthenia
    	'Eu46011',		#[X]Fatigue syndrome
    	'Eu46100',		#[X]Depersonalization - derealization syndrome
    	'Eu46y00',		#[X]Other specified neurotic disorders
    	'Eu46y11',		#[X]Briquet's disorder
    	'Eu46y12',		#[X]Dhat syndrome
    	'Eu46y13',		#[X]Occupational neurosis; including writer's cramp
    	'Eu46y14',		#[X]Psychasthenia
    	'Eu46y15',		#[X]Psychasthenia neurosis
    	'Eu46y16',		#[X]Psychogenic syncope
    	'Eu46z00',		#[X]Neurotic disorder; unspecified
    	'Eu46z11',		#[X]Neurosis NOS
    	'Eu51511',		#[X]Dream anxiety disorder
    	'Eu93000',		#[X]Separation anxiety disorder of childhood
    	'Eu93100',		#[X]Phobic anxiety disorder of childhood
    	'Eu93200',		#[X]Social anxiety disorder of childhood
    	'Eu93y12',		#[X]Childhood overanxious disorder
    	'Z4L1.00',		#Anxiety counselling
    	'ZS7C700',		#Post-traumatic mutism

        # Eating disorders
    	'1612',		#Appetite loss - anorexia
    	'1612.11',		#Anorexia symptom
    	'1614',		#Excessive eating - polyphagia
    	'1614.11',		#Hyperalimentation - symptom
    	'1614.12',		#Polyphagia symptom
    	'8HTN.00',		#Referral to eating disorders clinic
    	'9Nk9.00',		#Seen in eating disorder clinic
    	'E271.00',		#Anorexia nervosa
    	'E275.00',		#Other and unspecified non-organic eating disorders
    	'E275000',		#Unspecified non-organic eating disorder
    	'E275100',		#Bulimia (non-organic overeating)
    	'E275111',		#Compulsive eating disorder
    	'E275y00',		#Other specified non-organic eating disorder
    	'E275z00',		#Non-organic eating disorder NOS
    	'Eu50.00',		#[X]Eating disorders
    	'Eu50000',		#[X]Anorexia nervosa
    	'Eu50100',		#[X]Atypical anorexia nervosa
    	'Eu50200',		#[X]Bulimia nervosa
    	'Eu50211',		#[X]Bulimia NOS
    	'Eu50212',		#[X]Hyperorexia nervosa
    	'Eu50300',		#[X]Atypical bulimia nervosa
    	'Eu50400',		#[X]Overeating associated with other psychological disturbncs
    	'Eu50411',		#[X]Psychogenic overeating
    	'Eu50y00',		#[X]Other eating disorders
    	'Eu50y11',		#[X]Pica in adults
    	'Eu50z00',		#[X]Eating disorder; unspecified
    	'Fy05.00',		#Nocturnal sleep-related eating disorder
    	'R030.00',		#[D]Anorexia
    	'R030z00',		#[D]Anorexia NOS
    	'R036.00',		#[D]Polyphagia
    	'R036000',		#[D]Excessive eating
    	'R036011',		#[D]Bulimia NOS
    	'R036100',		#[D]Hyperalimentation
    	'R036z00',		#[D]Polyphagia NOS
    	'SN42100',		#Starvation
    	'U1B3.11',		#[X]Starvation
    	'Z4B5.00',		#Eating disorder counselling
    	'ZC2CD00',		#Dietary advice for eating disorder

        # Personality disorders
    	'E21..00',		#Personality disorders
    	'E210.00',		#Paranoid personality disorder
    	'E211.00',		#Affective personality disorder
    	'E211000',		#Unspecified affective personality disorder
    	'E21..11',		#Neurotic personality disorder
    	'E211100',		#Hypomanic personality disorder
    	'E211200',		#Depressive personality disorder
    	'E211300',		#Cyclothymic personality disorder
    	'E211z00',		#Affective personality disorder NOS
    	'E212.00',		#Schizoid personality disorder
    	'E212000',		#Unspecified schizoid personality disorder
    	'E212z00',		#Schizoid personality disorder NOS
    	'E213.00',		#Explosive personality disorder
    	'E214.00',		#Compulsive personality disorders
    	'E214000',		#Anankastic personality
    	'E214.11',		#Anancastic personality
    	'E214z00',		#Compulsive personality disorder NOS
    	'E215.00',		#Histrionic personality disorders
    	'E215000',		#Unspecified histrionic personality disorder
    	'E215.11',		#Hysterical personality disorders
    	'E215z00',		#Histrionic personality disorder NOS
    	'E216.00',		#Inadequate personality disorder
    	'E217.00',		#Antisocial or sociopathic personality disorder
    	'E21y.00',		#Other personality disorders
    	'E21y000',		#Narcissistic personality disorder
    	'E21y100',		#Avoidant personality disorder
    	'E21y200',		#Borderline personality disorder
    	'E21y300',		#Passive-aggressive personality disorder
    	'E21y400',		#Eccentric personality disorder
    	'E21y500',		#Immature personality disorder
    	'E21y600',		#Masochistic personality disorder
    	'E21y700',		#Psychoneurotic personality disorder
    	'E21yz00',		#Other personality disorder NOS
    	'E21z.00',		#Personality disorder NOS
    	'E21z.11',		#Psychopathic personality
    	'Eu06000',		#[X]Organic personality disorder
    	'Eu06011',		#[X]Organic pseudopsychopathic personality
    	'Eu21.17',		#[X]Pseudopsychopathic schizophrenia
    	'Eu21.18',		#[X]Schizotypal personality disorder
    	'Eu34011',		#[X]Affective personality disorder
    	'Eu34112',		#[X]Depressive personality disorder
    	'Eu60.00',		#[X]Specific personality disorders
    	'Eu60000',		#[X]Paranoid personality disorder
    	'Eu60013',		#[X]Querulant personality disorder
    	'Eu60014',		#[X]Sensitive paranoid personality disorder
    	'Eu60100',		#[X]Schizoid personality disorder
    	'Eu60200',		#[X]Dissocial personality disorder
    	'Eu60212',		#[X]Antisocial personality disorder
    	'Eu60213',		#[X]Asocial personality disorder
    	'Eu60214',		#[X]Psychopathic personality disorder
    	'Eu60215',		#[X]Sociopathic personality disorder
    	'Eu60300',		#[X]Emotionally unstable personality disorder
    	'Eu60311',		#[X]Aggressive personality disorder
    	'Eu60312',		#[X]Borderline personality disorder
    	'Eu60313',		#[X]Explosive personality disorder
    	'Eu60400',		#[X]Histrionic personality disorder
    	'Eu60411',		#[X]Hysterical personality disorder
    	'Eu60412',		#[X]Psychoinfantile personality disorder
    	'Eu60500',		#[X]Anankastic personality disorder
    	'Eu60511',		#[X]Compulsive personality disorder
    	'Eu60512',		#[X]Obsessional personality disorder
    	'Eu60513',		#[X]Obsessive-compulsive personality disorder
    	'Eu60600',		#[X]Anxious [avoidant] personality disorder
    	'Eu60700',		#[X]Dependent personality disorder
    	'Eu60711',		#[X]Asthenic personality disorder
    	'Eu60712',		#[X]Inadequate personality disorder
    	'Eu60713',		#[X]Passive personality disorder
    	'Eu60714',		#[X]Self defeating personality disorder
    	'Eu60y00',		#[X]Other specific personality disorders
    	'Eu60y11',		#[X]Eccentric personality disorder
    	'Eu60y12',		#[X]Haltlose type personality disorder
    	'Eu60y13',		#[X]Immature personality disorder
    	'Eu60y14',		#[X]Narcissistic personality disorder
    	'Eu60y16',		#[X]Psychoneurotic personality disorder
    	'Eu60z00',		#[X]Personality disorder; unspecified
    	'Eu61.00',		#[X]Mixed and other personality disorders
    	'Eu84511',		#[X]Autistic psychopathy
    	'Eu94211',		#[X]Affectionless psychopathy

        #DEPRESSION - non-severe (severe depression codes go in the mental_illness_SMI dict)
    	'1B17.00',		#Depressed
    	'2257',		    #O/E - depressed
    	'62T1.00',		#Puerperal depression
    	'9kQ..00',		#On full dose long term treatment depression - enh serv admin
    	'E001300',		#Presenile dementia with depression
    	'E002100',		#Senile dementia with depression
    	'E004300',		#Arteriosclerotic dementia with depression
    	'E11..12',		#Depressive psychoses
    	'E112.00',		#Single major depressive episode
    	'E112000',		#Single major depressive episode; unspecified
    	'E112100',		#Single major depressive episode; mild
    	'E112.11',		#Agitated depression
    	'E112.12',		#Endogenous depression first episode
    	'E112.13',		#Endogenous depression first episode
    	'E112.14',		#Endogenous depression
    	'E112200',		#Single major depressive episode; moderate

    	'E112z00',		#Single major depressive episode NOS
    	'E113.00',		#Recurrent major depressive episode
    	'E113000',		#Recurrent major depressive episodes; unspecified
    	'E113100',		#Recurrent major depressive episodes; mild
    	'E113.11',		#Endogenous depression - recurrent
    	'E113200',		#Recurrent major depressive episodes; moderate
    	'E113700',		#Recurrent depression
    	'E113z00',		#Recurrent major depressive episode NOS
    	'E118.00',		#Seasonal affective disorder
    	'E11y200',		#Atypical depressive disorder
    	'E11z200',		#Masked depression
    	'E135.00',		#Agitated depression
    	'E200300',		#Anxiety with depression
    	'E204.00',		#Neurotic depression reactive type
    	'E204.11',		#Postnatal depression
    	'E290.00',		#Brief depressive reaction
    	'E290z00',		#Brief depressive reaction NOS
    	'E291.00',		#Prolonged depressive reaction
    	'E2B..00',		#Depressive disorder NEC
    	'E2B0.00',		#Postviral depression
    	'E2B1.00',		#Chronic depression
    	'Eu20400',		#[X]Post-schizophrenic depression
    	'Eu32.00',		#[X]Depressive episode
    	'Eu32000',		#[X]Mild depressive episode
    	'Eu32100',		#[X]Moderate depressive episode
    	'Eu32.11',		#[X]Single episode of depressive reaction
    	'Eu32.12',		#[X]Single episode of psychogenic depression
    	'Eu32.13',		#[X]Single episode of reactive depression
    	'Eu32200',		#[X]Severe depressive episode without psychotic symptoms
    	'Eu32211',		#[X]Single episode agitated depressn w'out psychotic symptoms
    	'Eu32212',		#[X]Single episode major depression w'out psychotic symptoms
    	'Eu32213',		#[X]Single episode vital depression w'out psychotic symptoms
    	'Eu32400',		#[X]Mild depression
    	'Eu32500',		#[X]Major depression; mild
    	'Eu32600',		#[X]Major depression; moderately severe
    	'Eu32y00',		#[X]Other depressive episodes
    	'Eu32y11',		#[X]Atypical depression
    	'Eu32y12',		#[X]Single episode of masked depression NOS
    	'Eu32z00',		#[X]Depressive episode; unspecified
    	'Eu32z11',		#[X]Depression NOS
    	'Eu32z12',		#[X]Depressive disorder NOS
    	'Eu32z13',		#[X]Prolonged single episode of reactive depression
    	'Eu32z14',		#[X] Reactive depression NOS
    	'Eu33.00',		#[X]Recurrent depressive disorder
    	'Eu33000',		#[X]Recurrent depressive disorder; current episode mild
    	'Eu33100',		#[X]Recurrent depressive disorder; current episode moderate
    	'Eu33.11',		#[X]Recurrent episodes of depressive reaction
    	'Eu33.12',		#[X]Recurrent episodes of psychogenic depression
    	'Eu33.13',		#[X]Recurrent episodes of reactive depression
    	'Eu33.14',		#[X]Seasonal depressive disorder
    	'Eu33.15',		#[X]SAD - Seasonal affective disorder
    	'Eu33211',		#[X]Endogenous depression without psychotic symptoms
    	'Eu33212',		#[X]Major depression; recurrent without psychotic symptoms
    	'Eu33214',		#[X]Vital depression; recurrent without psychotic symptoms

    	'Eu33400',		#[X]Recurrent depressive disorder; currently in remission
    	'Eu33y00',		#[X]Other recurrent depressive disorders
    	'Eu33z00',		#[X]Recurrent depressive disorder; unspecified
    	'Eu33z11',		#[X]Monopolar depression NOS
    	'Eu34100',		#[X]Dysthymia
    	'Eu34111',		#[X]Depressive neurosis
    	'Eu34113',		#[X]Neurotic depression
    	'Eu34114',		#[X]Persistant anxiety depression
    	'Eu3y111',		#[X]Recurrent brief depressive episodes
    	'Eu41200',		#[X]Mixed anxiety and depressive disorder
    	'Eu41211',		#[X]Mild anxiety depression
    	'Eu53011',		#[X]Postnatal depression NOS
    	'Eu53012',		#[X]Postpartum depression NOS
    	'Eu92000'		#[X]Depressive conduct disorder
    ]
}

mental_illness_smi = {
    'name': 'mental_illness_smi',
    'codes': [
        #taken from https://clinicalcodes.rss.mhs.man.ac.uk/medcodes/article/38/

        #SEVERE OR PSYCHOTIC DEPRESSION
    	'Eu33300',		#[X]Recurrent depress disorder cur epi severe with psyc symp
    	'Eu33311',		#[X]Endogenous depression with psychotic symptoms
    	'Eu33312',		#[X]Manic-depress psychosis;depressed type+psychotic symptoms
    	'Eu33313',		#[X]Recurr severe episodes/major depression+psychotic symptom
    	'Eu33314',		#[X]Recurr severe episodes/psychogenic depressive psychosis
    	'Eu33315',		#[X]Recurrent severe episodes of psychotic depression
    	'Eu33316',		#[X]Recurrent severe episodes/reactive depressive psychosis
    	'Eu33200',		#[X]Recurr depress disorder cur epi severe without psyc sympt
        'Eu32700',		#[X]Major depression; severe without psychotic symptoms
    	'E112300',		#Single major depressive episode; severe; without psychosis
    	'E112400',		#Single major depressive episode; severe; with psychosis
    	'Eu32300',		#[X]Severe depressive episode with psychotic symptoms
    	'Eu32311',		#[X]Single episode of major depression and psychotic symptoms
    	'Eu32312',		#[X]Single episode of psychogenic depressive psychosis
    	'Eu32313',		#[X]Single episode of psychotic depression
    	'Eu32314',		#[X]Single episode of reactive depressive psychosis
    	'Eu32800',		#[X]Major depression; severe with psychotic symptoms
    	'Eu32900',		#[X]Single major depr ep; severe with psych; psych in remiss
    	'Eu32A00',		#[X]Recurr major depr ep; severe with psych; psych in remiss
    	'E113300',		#Recurrent major depressive episodes; severe; no psychosis
    	'E113400',		#Recurrent major depressive episodes; severe; with psychosis

        # BIPOLAR DISORDER
    	'146D.00',		#H/O: manic depressive disorder
    	'1S42.00',		#Manic mood
    	'6657',		    #On lithium
    	'6657.11',		#Lithium monitoring
    	'6657.12',		#Started lithium
    	'E11..00',		#Affective psychoses
    	'E110.00',		#Manic disorder; single episode
    	'E110000',		#Single manic episode; unspecified
    	'E110100',		#Single manic episode; mild
    	'E110.11',		#Hypomanic psychoses
    	'E110200',		#Single manic episode; moderate
    	'E110300',		#Single manic episode; severe without mention of psychosis
    	'E110400',		#Single manic episode; severe; with psychosis
    	'E110600',		#Single manic episode in full remission
    	'E110z00',		#Manic disorder; single episode NOS
    	'E111.00',		#Recurrent manic episodes
    	'E111000',		#Recurrent manic episodes; unspecified
    	'E11..11',		#Bipolar psychoses
    	'E111100',		#Recurrent manic episodes; mild
    	'E111200',		#Recurrent manic episodes; moderate
    	'E11..13',		#Manic psychoses
    	'E111300',		#Recurrent manic episodes; severe without mention psychosis
    	'E111400',		#Recurrent manic episodes; severe; with psychosis
    	'E111500',		#Recurrent manic episodes; partial or unspecified remission
    	'E111600',		#Recurrent manic episodes; in full remission
    	'E111z00',		#Recurrent manic episode NOS
    	'E114.00',		#Bipolar affective disorder; currently manic
    	'E114000',		#Bipolar affective disorder; currently manic; unspecified
    	'E114100',		#Bipolar affective disorder; currently manic; mild
    	'E114.11',		#Manic-depressive - now manic
    	'E114200',		#Bipolar affective disorder; currently manic; moderate
    	'E114300',		#Bipolar affect disord; currently manic; severe; no psychosis
    	'E114400',		#Bipolar affect disord; currently manic;severe with psychosis
    	'E114500',		#Bipolar affect disord;currently manic; part/unspec remission
    	'E114600',		#Bipolar affective disorder; currently manic; full remission
    	'E114z00',		#Bipolar affective disorder; currently manic; NOS
    	'E115.00',		#Bipolar affective disorder; currently depressed
    	'E115000',		#Bipolar affective disorder; currently depressed; unspecified
    	'E115100',		#Bipolar affective disorder; currently depressed; mild
    	'E115.11',		#Manic-depressive - now depressed
    	'E115200',		#Bipolar affective disorder; currently depressed; moderate
    	'E115300',		#Bipolar affect disord; now depressed; severe; no psychosis
    	'E115400',		#Bipolar affect disord; now depressed; severe with psychosis
    	'E115500',		#Bipolar affect disord; now depressed; part/unspec remission
    	'E115600',		#Bipolar affective disorder; now depressed; in full remission
    	'E115z00',		#Bipolar affective disorder; currently depressed; NOS
    	'E116.00',		#Mixed bipolar affective disorder
    	'E116000',		#Mixed bipolar affective disorder; unspecified
    	'E116100',		#Mixed bipolar affective disorder; mild
    	'E116200',		#Mixed bipolar affective disorder; moderate
    	'E116300',		#Mixed bipolar affective disorder; severe; without psychosis
    	'E116400',		#Mixed bipolar affective disorder; severe; with psychosis
    	'E116500',		#Mixed bipolar affective disorder; partial/unspec remission
    	'E116600',		#Mixed bipolar affective disorder; in full remission
    	'E116z00',		#Mixed bipolar affective disorder; NOS
    	'E117.00',		#Unspecified bipolar affective disorder
    	'E117000',		#Unspecified bipolar affective disorder; unspecified
    	'E117100',		#Unspecified bipolar affective disorder; mild
    	'E117200',		#Unspecified bipolar affective disorder; moderate
    	'E117300',		#Unspecified bipolar affective disorder; severe; no psychosis
    	'E117400',		#Unspecified bipolar affective disorder;severe with psychosis
    	'E117500',		#Unspecified bipolar affect disord; partial/unspec remission
    	'E117600',		#Unspecified bipolar affective disorder; in full remission
    	'E117z00',		#Unspecified bipolar affective disorder; NOS
    	'E11y.00',		#Other and unspecified manic-depressive psychoses
    	'E11y000',		#Unspecified manic-depressive psychoses
    	'E11y100',		#Atypical manic disorder
    	'E11y300',		#Other mixed manic-depressive psychoses
    	'E11yz00',		#Other and unspecified manic-depressive psychoses NOS
    	'Eu3..00',		#[X]Mood - affective disorders
    	'Eu30.00',		#[X]Manic episode
    	'Eu30000',		#[X]Hypomania
    	'Eu30100',		#[X]Mania without psychotic symptoms
    	'Eu30.11',		#[X]Bipolar disorder; single manic episode
    	'Eu30200',		#[X]Mania with psychotic symptoms
    	'Eu30211',		#[X]Mania with mood-congruent psychotic symptoms
    	'Eu30212',		#[X]Mania with mood-incongruent psychotic symptoms
    	'Eu30y00',		#[X]Other manic episodes
    	'Eu30z00',		#[X]Manic episode; unspecified
    	'Eu30z11',		#[X]Mania NOS
    	'Eu31.00',		#[X]Bipolar affective disorder
    	'Eu31000',		#[X]Bipolar affective disorder; current episode hypomanic
    	'Eu31100',		#[X]Bipolar affect disorder cur epi manic wout psychotic symp
    	'Eu31.11',		#[X]Manic-depressive illness
    	'Eu31.12',		#[X]Manic-depressive psychosis
    	'Eu31.13',		#[X]Manic-depressive reaction
    	'Eu31200',		#[X]Bipolar affect disorder cur epi manic with psychotic symp
    	'Eu31300',		#[X]Bipolar affect disorder cur epi mild or moderate depressn
    	'Eu31400',		#[X]Bipol aff disord; curr epis sev depress; no psychot symp
    	'Eu31500',		#[X]Bipolar affect dis cur epi severe depres with psyc symp
    	'Eu31600',		#[X]Bipolar affective disorder; current episode mixed
    	'Eu31700',		#[X]Bipolar affective disorder; currently in remission
    	'Eu31y00',		#[X]Other bipolar affective disorders
    	'Eu31y11',		#[X]Bipolar II disorder
    	'Eu31y12',		#[X]Recurrent manic episodes
    	'Eu31z00',		#[X]Bipolar affective disorder; unspecified
    	'Eu33213',		#[X]Manic-depress psychosis;depressd;no psychotic symptoms
    	'Eu33312',		#[X]Manic-depress psychosis;depressed type+psychotic symptoms
    	'Eu34.00',		#[X]Persistent mood affective disorders
    	'Eu34000',		#[X]Cyclothymia
    	'Eu34y00',		#[X]Other persistent mood affective disorders
    	'Eu34z00',		#[X]Persistent mood affective disorder; unspecified
    	'Eu3y.00',		#[X]Other mood affective disorders
    	'Eu3y000',		#[X]Other single mood affective disorders
    	'Eu3y011',		#[X]Mixed affective episode
    	'Eu3y100',		#[X]Other recurrent mood affective disorders
    	'Eu3yy00',		#[X]Other specified mood affective disorders
    	'Eu3z.00',		#[X]Unspecified mood affective disorder
    	'Eu3z.11',		#[X]Affective psychosis NOS
    	'ZV11111',		#[V]Personal history of manic-depressive psychosis
    	'ZV11112',		#[V]Personal history of manic-depressive psychosis

        # SCHIZOPHRENIA SPECTRUM
    	'1464',		#H/O: schizophrenia
    	'146H.00',		#H/O: psychosis
    	'1BH..00',		#Delusions
    	'1BH0.00',		#Delusion of persecution
    	'1BH1.00',		#Grandiose delusions
    	'1BH..11',		#Delusion
    	'1BH2.00',		#Ideas of reference
    	'1BH3.00',		#Paranoid ideation
    	'225E.00',		#O/E - paranoid delusions
    	'225F.00',		#O/E - delusion of persecution
    	'285..11',		#Psychotic condition; insight present
    	'286..11',		#Poor insight into psychotic condition
    	'665E.00',		#Injectable neuroleptic given
    	'665F.00',		#On injectable neuroleptic
    	'E1...00',		#Non-organic psychoses
    	'E10..00',		#Schizophrenic disorders
    	'E100.00',		#Simple schizophrenia
    	'E100000',		#Unspecified schizophrenia
    	'E100100',		#Subchronic schizophrenia
    	'E100.11',		#Schizophrenia simplex
    	'E100200',		#Chronic schizophrenic
    	'E100300',		#Acute exacerbation of subchronic schizophrenia
    	'E100400',		#Acute exacerbation of chronic schizophrenia
    	'E100500',		#Schizophrenia in remission
    	'E100z00',		#Simple schizophrenia NOS
    	'E101.00',		#Hebephrenic schizophrenia
    	'E101000',		#Unspecified hebephrenic schizophrenia
    	'E101400',		#Acute exacerbation of chronic hebephrenic schizophrenia
    	'E101500',		#Hebephrenic schizophrenia in remission
    	'E101z00',		#Hebephrenic schizophrenia NOS
    	'E102.00',		#Catatonic schizophrenia
    	'E102000',		#Unspecified catatonic schizophrenia
    	'E102100',		#Subchronic catatonic schizophrenia
    	'E102500',		#Catatonic schizophrenia in remission
    	'E102z00',		#Catatonic schizophrenia NOS
    	'E103.00',		#Paranoid schizophrenia
    	'E103000',		#Unspecified paranoid schizophrenia
    	'E103200',		#Chronic paranoid schizophrenia
    	'E103300',		#Acute exacerbation of subchronic paranoid schizophrenia
    	'E103400',		#Acute exacerbation of chronic paranoid schizophrenia
    	'E103500',		#Paranoid schizophrenia in remission
    	'E103z00',		#Paranoid schizophrenia NOS
    	'E104.00',		#Acute schizophrenic episode
    	'E105.00',		#Latent schizophrenia
    	'E105000',		#Unspecified latent schizophrenia
    	'E105200',		#Chronic latent schizophrenia
    	'E105500',		#Latent schizophrenia in remission
    	'E105z00',		#Latent schizophrenia NOS
    	'E106.00',		#Residual schizophrenia
    	'E107.00',		#Schizo-affective schizophrenia
    	'E107000',		#Unspecified schizo-affective schizophrenia
    	'E107100',		#Subchronic schizo-affective schizophrenia
    	'E107.11',		#Cyclic schizophrenia
    	'E107200',		#Chronic schizo-affective schizophrenia
    	'E107300',		#Acute exacerbation subchronic schizo-affective schizophrenia
    	'E107400',		#Acute exacerbation of chronic schizo-affective schizophrenia
    	'E107500',		#Schizo-affective schizophrenia in remission
    	'E107z00',		#Schizo-affective schizophrenia NOS
    	'E10y.00',		#Other schizophrenia
    	'E10y000',		#Atypical schizophrenia
    	'E10y100',		#Coenesthopathic schizophrenia
    	'E10y.11',		#Cenesthopathic schizophrenia
    	'E10yz00',		#Other schizophrenia NOS
    	'E10z.00',		#Schizophrenia NOS
    	'E11z.00',		#Other and unspecified affective psychoses
    	'E11z000',		#Unspecified affective psychoses NOS
    	'E11zz00',		#Other affective psychosis NOS
    	'E12..00',		#Paranoid states
    	'E120.00',		#Simple paranoid state
    	'E121.00',		#Chronic paranoid psychosis
    	'E122.00',		#Paraphrenia
    	'E123.00',		#Shared paranoid disorder
    	'E12y.00',		#Other paranoid states
    	'E12y000',		#Paranoia querulans
    	'E12yz00',		#Other paranoid states NOS
    	'E12z.00',		#Paranoid psychosis NOS
    	'E13..00',		#Other nonorganic psychoses
    	'E130.00',		#Reactive depressive psychosis
    	'E130.11',		#Psychotic reactive depression
    	'E131.00',		#Acute hysterical psychosis
    	'E13..11',		#Reactive psychoses
    	'E133.00',		#Acute paranoid reaction
    	'E134.00',		#Psychogenic paranoid psychosis
    	'E13y.00',		#Other reactive psychoses
    	'E13y100',		#Brief reactive psychosis
    	'E13yz00',		#Other reactive psychoses NOS
    	'E13z.00',		#Nonorganic psychosis NOS
    	'E13z.11',		#Psychotic episode NOS
    	'E14..00',		#Psychoses with origin in childhood
    	'E141.00',		#Disintegrative psychosis
    	'E141100',		#Residual disintegrative psychoses
    	'E141.11',		#Heller's syndrome
    	'E1y..00',		#Other specified non-organic psychoses
    	'E1z..00',		#Non-organic psychosis NOS
    	'Eu02z12',		#[X] Presenile psychosis NOS
    	'Eu0z.12',		#[X]Symptomatic psychosis NOS
    	'Eu2..00',		#[X]Schizophrenia; schizotypal and delusional disorders
    	'Eu20.00',		#[X]Schizophrenia
    	'Eu20000',		#[X]Paranoid schizophrenia
    	'Eu20011',		#[X]Paraphrenic schizophrenia
    	'Eu20100',		#[X]Hebephrenic schizophrenia
    	'Eu20111',		#[X]Disorganised schizophrenia
    	'Eu20200',		#[X]Catatonic schizophrenia
    	'Eu20211',		#[X]Catatonic stupor
    	'Eu20212',		#[X]Schizophrenic catalepsy
    	'Eu20213',		#[X]Schizophrenic catatonia
    	'Eu20214',		#[X]Schizophrenic flexibilatis cerea
    	'Eu20300',		#[X]Undifferentiated schizophrenia
    	'Eu20311',		#[X]Atypical schizophrenia
    	'Eu20500',		#[X]Residual schizophrenia
    	'Eu20511',		#[X]Chronic undifferentiated schizophrenia
    	'Eu20600',		#[X]Simple schizophrenia
    	'Eu20y00',		#[X]Other schizophrenia
    	'Eu20y12',		#[X]Schizophreniform disord NOS
    	'Eu20y13',		#[X]Schizophrenifrm psychos NOS
    	'Eu20z00',		#[X]Schizophrenia; unspecified
    	'Eu21.00',		#[X]Schizotypal disorder
    	'Eu21.11',		#[X]Latent schizophrenic reaction
    	'Eu21.12',		#[X]Borderline schizophrenia
    	'Eu21.13',		#[X]Latent schizophrenia
    	'Eu21.14',		#[X]Prepsychotic schizophrenia
    	'Eu21.15',		#[X]Prodromal schizophrenia
    	'Eu21.16',		#[X]Pseudoneurotic schizophrenia
    	'Eu22.00',		#[X]Persistent delusional disorders
    	'Eu22000',		#[X]Delusional disorder
    	'Eu22011',		#[X]Paranoid psychosis
    	'Eu22012',		#[X]Paranoid state
    	'Eu22013',		#[X]Paraphrenia - late
    	'Eu22014',		#[X]Sensitiver Beziehungswahn
    	'Eu22015',		#[X]Paranoia
    	'Eu22100',		#[X]Delusional misidentification syndrome
    	'Eu22111',		#[X]Capgras syndrome
    	'Eu22y00',		#[X]Other persistent delusional disorders
    	'Eu22y11',		#[X]Delusional dysmorphophobia
    	'Eu22y12',		#[X]Involutional paranoid state
    	'Eu22y13',		#[X]Paranoia querulans
    	'Eu22z00',		#[X]Persistent delusional disorder; unspecified
    	'Eu23.00',		#[X]Acute and transient psychotic disorders
    	'Eu23000',		#[X]Acute polymorphic psychot disord without symp of schizoph
    	'Eu23012',		#[X]Cycloid psychosis
    	'Eu23100',		#[X]Acute polymorphic psychot disord with symp of schizophren
    	'Eu23112',		#[X]Cycloid psychosis with symptoms of schizophrenia
    	'Eu23200',		#[X]Acute schizophrenia-like psychotic disorder
    	'Eu23211',		#[X]Brief schizophreniform disorder
    	'Eu23212',		#[X]Brief schizophrenifrm psych
    	'Eu23214',		#[X]Schizophrenic reaction
    	'Eu23300',		#[X]Other acute predominantly delusional psychotic disorders
    	'Eu23312',		#[X]Psychogenic paranoid psychosis
    	'Eu23y00',		#[X]Other acute and transient psychotic disorders
    	'Eu23z00',		#[X]Acute and transient psychotic disorder; unspecified
    	'Eu23z11',		#[X]Brief reactive psychosis NOS
    	'Eu23z12',		#[X]Reactive psychosis
    	'Eu25.00',		#[X]Schizoaffective disorders
    	'Eu25000',		#[X]Schizoaffective disorder; manic type
    	'Eu25011',		#[X]Schizoaffective psychosis; manic type
    	'Eu25012',		#[X]Schizophreniform psychosis; manic type
    	'Eu25100',		#[X]Schizoaffective disorder; depressive type
    	'Eu25111',		#[X]Schizoaffective psychosis; depressive type
    	'Eu25112',		#[X]Schizophreniform psychosis; depressive type
    	'Eu25200',		#[X]Schizoaffective disorder; mixed type
    	'Eu25212',		#[X]Mixed schizophrenic and affective psychosis
    	'Eu25y00',		#[X]Other schizoaffective disorders
    	'Eu25z00',		#[X]Schizoaffective disorder; unspecified
    	'Eu25z11',		#[X]Schizoaffective psychosis NOS
    	'Eu2y.00',		#[X]Other nonorganic psychotic disorders
    	'Eu2y.11',		#[X]Chronic hallucinatory psychosis
    	'Eu2z.00',		#[X]Unspecified nonorganic psychosis
    	'Eu2z.11',		#[X]Psychosis NOS
    	'Eu32300',		#[X]Severe depressive episode with psychotic symptoms
    	'Eu32311',		#[X]Single episode of major depression and psychotic symptoms
    	'Eu32312',		#[X]Single episode of psychogenic depressive psychosis
    	'Eu32313',		#[X]Single episode of psychotic depression
    	'Eu32314',		#[X]Single episode of reactive depressive psychosis
    	'Eu32900',		#[X]Single major depr ep; severe with psych; psych in remiss
    	'Eu32A00',		#[X]Recurr major depr ep; severe with psych; psych in remiss
    	'Eu33300',		#[X]Recurrent depress disorder cur epi severe with psyc symp
    	'Eu33311',		#[X]Endogenous depression with psychotic symptoms
    	'Eu33313',		#[X]Recurr severe episodes/major depression+psychotic symptom
    	'Eu33314',		#[X]Recurr severe episodes/psychogenic depressive psychosis
    	'Eu33315',		#[X]Recurrent severe episodes of psychotic depression
    	'Eu33316',		#[X]Recurrent severe episodes/reactive depressive psychosis
    	'Eu44.14',		#[X]Hysterical psychosis
    	'Eu84312',		#[X]Disintegrative psychosis
    	'Eu84314',		#[X]Symbiotic psychosis
    	'R001.00',		#[D]Hallucinations
    	'R001000',		#[D]Hallucinations; auditory
    	'R001100',		#[D]Hallucinations; gustatory
    	'R001200',		#[D]Hallucinations; olfactory
    	'R001300',		#[D]Hallucinations; tactile
    	'R001400',		#[D]Visual hallucinations
    	'R001z00',		#[D]Hallucinations NOS
    	'Ryu5300',		#[X]Other hallucinations
    	'ZS7C611',		#Schizophrenic language
    	'ZV11000'	#[V]Personal history of schizophrenia
    ]
}


sleep_apnoea = {
    'name': 'sleep_apnoea',
    'codes': [
    	'H5B0.00',		#Obstructive sleep apnoea
    	'R005100',		#[D]Insomnia with sleep apnoea
    	'R005312',		#[D]Syndrome sleep apnoea
    	'R005311',		#[D]Sleep apnoea syndrome
    	'R060400',		#[D]Apnoea
    	'R005300',		#[D]Hypersomnia with sleep apnoea
    	'Fy03.11',		#Obstructive sleep apnoea
    	'H5B..00',		#Sleep apnoea
    	'Fy03.00'		#Sleep apnoea
    ]
}
