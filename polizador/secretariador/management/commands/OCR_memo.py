import os
import typing_extensions as typing
import json
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore
from google.api_core.exceptions import FailedPrecondition, NotFound
from typing import Optional
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from secretariador.functions import FileValidator
from secretariador.models import Solicitud, Comisionado, generate_name_resoluciones, InstrumentosLegalesMemorandum
import time

class Resolucion(typing.TypedDict):
  numero_de_resolucion: int
  año_de_la_resolucion: int
  fecha_de_la_resolucion: str
  numero_de_actuacion: int
  año_de_la_actuacion: int
  a_traves_de_quien_se_ejecutaran_los_trabajos: str
  los_trabajos_a_realizar: str
  monto_de_los_trabajos: float
  nombre_del_programa_marco: str

# TODO(developer): Uncomment these variables before running the sample.
project_id = 'gen-lang-client-0374726319'
location = 'us' # Format is 'us' or 'eu'
processor_display_name = 'test_processor_ocr_processor' # Must be unique per project, e.g.: 'My Processor'
processor_type = 'OCR_PROCESSOR' # Use fetch_processor_types to get available processor types
processor_id_summary = 'd7c3475c0c92e6e3'
processor_id = 'bc2556a92e4b120a'
file_path = ""
dir_path = "/home/willy/memorandum2024/"
mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
# processor_version_id = "YOUR_PROCESSOR_VERSION_ID" # Optional. Processor version to use
test_file_uri = "gs://polizador-production-pdf/instrumentoslegales/resoluciones/"

def fetch_processor_types_sample(project_id: str, location: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location
    parent = client.common_location_path(project_id, location)

    # Fetch all processor types
    response = client.fetch_processor_types(parent=parent)

    print("Processor types:")
    # Print the available processor types
    for processor_type in response.processor_types:
        if processor_type.allow_creation:
            print(processor_type.type_)

def create_processor_sample(
    project_id: str, location: str, processor_display_name: str, processor_type: str
) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location
    parent = client.common_location_path(project_id, location)

    # Create a processor
    processor = client.create_processor(
        parent=parent,
        processor=documentai.Processor(
            display_name=processor_display_name, type_=processor_type
        ),
    )

    # Print the processor information
    print(f"Processor Name: {processor.name}")
    print(f"Processor Display Name: {processor.display_name}")
    print(f"Processor Type: {processor.type_}")

def enable_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)
    request = documentai.EnableProcessorRequest(name=processor_name)

    # Make EnableProcessor request
    try:
        operation = client.enable_processor(request=request)

        # Print operation name
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    # Cannot enable a processor that is already enabled
    except FailedPrecondition as e:
        print(e.message)

def delete_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)

    # Delete a processor
    try:
        operation = client.delete_processor(name=processor_name)
        # Print operation details
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    except NotFound as e:
        print(e.message)

def process_document_sample(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str, field_mask: Optional[str] = None, processor_version_id: Optional[str] = None,) -> None:
    # You must set the `api_endpoint` if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    if processor_version_id:
        # The full resource name of the processor version, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
        name = client.processor_version_path(
            project_id, location, processor_id, processor_version_id
        )
    else:
        # The full resource name of the processor, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}`
        name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # For more information: https://cloud.google.com/document-ai/docs/reference/rest/v1/ProcessOptions
    # Optional: Additional configurations for processing.
    process_options = documentai.ProcessOptions(
        # Process only specific pages
        # individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
        #     pages=[1]
        # )
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=field_mask,
        process_options=process_options,
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    document = result.document

    # Read the text recognition output from the processor
    return document

# document = process_document_sample(project_id, location, processor_id, file_path, mime_type)
# document.text

#     def ERROR(self, text: str) -> str: ...
#     def SUCCESS(self, text: str) -> str: ...
#     def WARNING(self, text: str) -> str: ...
#     def NOTICE(self, text: str) -> str: ...
#     def SQL_FIELD(self, text: str) -> str: ...
#     def SQL_COLTYPE(self, text: str) -> str: ...
#     def SQL_KEYWORD(self, text: str) -> str: ...
#     def SQL_TABLE(self, text: str) -> str: ...
#     def HTTP_INFO(self, text: str) -> str: ...
#     def HTTP_SUCCESS(self, text: str) -> str: ...
#     def HTTP_REDIRECT(self, text: str) -> str: ...
#     def HTTP_NOT_MODIFIED(self, text: str) -> str: ...
#     def HTTP_BAD_REQUEST(self, text: str) -> str: ...
#     def HTTP_NOT_FOUND(self, text: str) -> str: ...
#     def HTTP_SERVER_ERROR(self, text: str) -> str: ...
#     def MIGRATE_HEADING(self, text: str) -> str: ...
#     def MIGRATE_LABEL(self, text: str) -> str: ...
#     def ERROR_OUTPUT(self, text: str) -> str: ...

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        pdf_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.pdf')]

        pdf_files.sort()
        for file in pdf_files[:2]:
            start_time = time.perf_counter()
            filename = os.path.basename(file)
            filename = filename.replace(".pdf", "")
            res_number = str(int(filename.split(" ")[4])).zfill(4) # Convert to int so we can be sure is the correct number, and then to string, then fill with zero to 4 digits.
            res_year = "2024"

            file_object = File(open(file, "rb"))
            self.stdout.write(f"{self.style.MIGRATE_LABEL('Procesando el archivo:')} {self.style.SQL_KEYWORD(file)}")
            print(res_number, res_year)

            p, created = InstrumentosLegalesMemorandum.objects.get_or_create(
                instrumentolegalmemorandum_numero=res_number,
                instrumentolegalmemorandum_ano=res_year,
                defaults={
                    "instrumentolegalmemorandum_tipo":"P",
                    "instrumentolegalmemorandum_descripcion":"Memorandum importado por OCR",
                    "instrumentolegalmemorandum_autocarga":True,
                    "instrumentolegalmemorandum":file_object
                }
                )
            if created:
                try:
                    self.stdout.write(f"{self.style.MIGRATE_LABEL('Procesando OCR:')}")
                    document = process_document_sample(project_id, location, processor_id, file, mime_type)
                    p.instrumentolegalmemorandum_document = document.text
                    p.save()
                    # json_document = documentai.Document.to_json(document)
                except Exception as e:
                    self.stdout.write(f"Error al procesar el archivo {self.style.ERROR(file)}: {self.style.ERROR(e)}")
                    continue
                self.stdout.write(f"{self.style.SUCCESS('Archivo procesado con éxito.')}")

                self.stdout.write(f"{self.style.MIGRATE_LABEL('Entrada creada:')}")
                self.stdout.write(f"    ID:{p.id}")
                self.stdout.write(f"    Memorandum de Presidencia Nº:{p.instrumentolegalmemorandum_numero}/{p.instrumentolegalmemorandum_ano}")
                self.stdout.write(f"    Fecha de Aprobación: {p.instrumentolegalmemorandum_fecha_aprobacion}")
                self.stdout.write(f"    Descripción: {p.instrumentolegalmemorandum_descripcion}")
                self.stdout.write(f"    Texto Extraído: {self.style.HTTP_SUCCESS(p.instrumentolegalmemorandum_document[:100])}...(truncado)")
                self.stdout.write(f"...")
                self.stdout.write(f"    Archivo subido: {self.style.SUCCESS(p.instrumentolegalmemorandum)}")

            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            self.stdout.write(f"Tiempo de ejecución: {elapsed_time:.6f} segundos.")
