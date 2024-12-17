import logging

from src.Extraction_engine import ExtractionEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(filename)s:%(lineno)d] - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    ext_engine_inst = ExtractionEngine()
    # V1
    # print(ext_engine_inst.process_pdf_v1(pdf_path="Posco_Logistics.pdf"))
    # V2
    print(ext_engine_inst.process_pdf(pdf_path="Posco_Logistics.pdf"))



# V1 output = {
#   "booking_details": {
#     "booking_number": {
#       "value": "POSU6396610410",
#       "confidence": 0.9760273098945618
#     },
#     "service_contract_number": {
#       "value": "APT24017",
#       "confidence": 0.9939196109771729
#     }
#   },
#   "shipment_route": {
#     "origin": {
#       "value": "China",
#       "confidence": 1.0
#     },
#     "destination": {
#       "value": "Fremantle, Western Australia",
#       "confidence": 0.9667136669158936
#     },
#     "transit_ports": {
#       "value": "Singapore / Pasir Panjang",
#       "confidence": 0.9624230861663818
#     }
#   },
#   "cargo_information": {
#     "cargo_type": {
#       "value": "General",
#       "confidence": 0.9540015459060669
#     },
#     "cargo_description": {
#       "value": "Chemical Absorbent Pad",
#       "confidence": 1.0
#     },
#     "container_details": {
#       "value": "container_details: 1 X 40' Hi-Cube Container",
#       "confidence": 1.0
#     },
#     "total_weight": {
#       "value": "6000 KG",
#       "confidence": 1.0
#     }
#   },
#   "vessel_information": {
#     "vessel_name": {
#       "value": "XIN HUI ZHOU",
#       "confidence": 0.9848887920379639
#     },
#     "vessel_voyage": {
#       "value": "XIN HUI ZHOU",
#       "confidence": 0.9660152792930603
#     },
#     "estimated_departure": {
#       "value": "04 Oct 2024 01:00(CST)",
#       "confidence": 1.0
#     },
#     "estimated_arrival": {
#       "value": "25 Oct 2024 14:00",
#       "confidence": 0.9547117352485657
#     }
#   },
#   "parties_information": {
#     "shipper": {
#       "value": "Winmore Logistics China Limited",
#       "confidence": 0.9961995482444763
#     },
#     "carrier": {
#       "value": "Winmore Logistics China Limited",
#       "confidence": 0.9299182295799255
#     }
#   }
# }

# V2 Output {
#   "booking_details": {
#     "booking_number": {
#       "value": "POSU6396610410",
#       "confidence": 0.9739648103713989
#     },
#     "service_contract_number": {
#       "value": "APT24017",
#       "confidence": 0.988732099533081
#     }
#   },
#   "shipment_route": {
#     "origin": {
#       "location": {
#         "value": "Singapore / Pasir Panjang",
#         "confidence": 1
#       },
#       "terminal": {
#         "value": "Singapore / Pasir Panjang",
#         "confidence": 1
#       }
#     },
#     "destination": {
#       "location": {
#         "value": "Fremantle, Western Australia",
#         "confidence": 0.9570125937461853
#       },
#       "terminal": {
#         "value": "Fremantle / DP World",
#         "confidence": 1
#       }
#     },
#     "transit_ports": {
#       "answer": [
#         {
#           "port_name": {
#             "text": "Singapore",
#             "score": 0.8
#           },
#           "eta": {
#             "text": "16 Oct 2024 18:00",
#             "score": 0.8
#           }
#         },
#         {
#           "port_name": {
#             "text": "Fremantle",
#             "score": 0.7
#           },
#           "eta": {
#             "text": "25 Oct 2024 14:00",
#             "score": 0.7
#           }
#         }
#       ]
#     }
#   },
#   "cargo_information": {
#     "cargo_type": {
#       "value": "General",
#       "confidence": 1
#     },
#     "cargo_description": {
#       "value": "Chemical absorbent pad",
#       "confidence": 1
#     },
#     "container_details": {
#       "quantity": {
#         "value": "1",
#         "confidence": 1
#       },
#       "size": {
#         "value": "1 X 40'",
#         "confidence": 0.9131621718406677
#       },
#       "type": {
#         "value": "dict",
#         "confidence": 1
#       }
#     },
#     "total_weight": {
#       "value": "6000 KG",
#       "confidence": 1
#     }
#   },
#   "vessel_information": {
#     "vessel_name": {
#       "value": "XIN HUI ZHOU",
#       "confidence": 0.9736180901527405
#     },
#     "vessel_voyage": {
#       "value": "XIN HUI ZHOU 190S",
#       "confidence": 1
#     },
#     "estimated_departure": {
#       "value": "04 Oct 2024 21:00",
#       "confidence": 0.9194890856742859
#     },
#     "estimated_arrival": {
#       "value": "04 Oct 2024 01:00(CST)",
#       "confidence": 1
#     }
#   },
#   "parties_information": {
#     "shipper": {
#       "name": {
#         "value": "Winmore Logistics China Limited",
#         "confidence": 1
#       },
#       "contact_details": {
#         "value": "TEL: 4029601910 EMAIL: csat.beijing@poscon.com",
#         "confidence": 1
#       }
#     },
#     "carrier": {
#       "name": {
#         "value": "PARTIES INFORMATION",
#         "confidence": 1
#       },
#       "contact_details": {
#         "value": "TEL: 4029601910 EMAIL: csat.beijing@poscon.com",
#         "confidence": 1
#       }
#     }
#   }
# }