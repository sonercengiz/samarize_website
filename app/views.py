from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from app.scripts.convert_file import *
from app.scripts.samarize import remove_parantheses_sentences
from app.scripts.make_summary import summary

# Create your views here.
def index(request):
    template = "index.html"

    # if request.method == "POST":
    #     for file in request.FILES:
    #         if(file == "fileAbstract"):
    #             myFile = request.FILES["fileAbstract"]
    #         elif(file == "fileIntroduction"):
    #             myFile = request.FILES["fileIntroduction"]
    #         elif(file == "fileReview"):
    #             myFile = request.FILES["fileReview"]

    #     test = """Sound information is encoded as a series of spikes of the auditory nerve fibers (ANFs), and then transmitted to the brainstem auditory nuclei. Features such as timing and level are extracted from ANFs activity and further processed as the interaural time difference (ITD) and the interaural level difference (ILD), respectively. These two interaural difference cues are used for sound source localization by behaving animals. Both cues depend on the head size of animals and are extremely small, requiring specialized neural properties in order to process these cues with precision. Moreover, the sound level and timing cues are not processed independently from one another. Neurons in the nucleus angularis (NA) are specialized for coding sound level information in birds and the ILD is processed in the posterior part of the dorsal lateral lemniscus nucleus (LLDp). Processing of ILD is affected by the phase difference of binaural sound. Temporal features of sound are encoded in the pathway starting in nucleus magnocellularis (NM), and ITD is processed in the nucleus laminaris (NL). In this pathway a variety of specializations are found in synapse morphology, neuronal excitability, distribution of ion channels and receptors along the tonotopic axis, which reduces spike timing fluctuation in the ANFs-NM synapse, and imparts precise and stable ITD processing to the NL. Moreover, the contrast of ITD processing in NL is enhanced over a wide range of sound level through the activity of GABAergic inhibitory systems from both the superior olivary nucleus (SON) and local inhibitory neurons that follow monosynaptic to NM activity."""
    #     fileContext = file2text(myFile)
    #     fileContextNew = (fileContext)
    #     testNew = summary(test)
    #     context = { 
    #         "fileName": myFile.name,
    #         "file": test,
    #         "fileNew": testNew
    #     }
    #     return render(request, template, context)

    if request.method == "POST":
        text = request.POST['AbstractText']
        summarized = summary(remove_parantheses_sentences(text))

        context = { 
            "data": "Samarize",
            "lenOfOrgText": "Length of original text: " + str(len(text)),
            "originalText": text,
            "infoOfSummary": "Length of summary: " + str(len(summarized)) + ",\nReduction: %" + str(round(((1-len(summarized)/len(text))*100), 2)),
            "summary": summarized
        }
        return render(request, template, context)

    if request.method == "GET":

        context = {
            "data": "Samarize"
        }
        return render(request, template, context)