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