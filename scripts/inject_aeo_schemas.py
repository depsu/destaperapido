#!/usr/bin/env python3
"""
Inyecta FAQPage schema en páginas de /servicios/ y /blog/ que aún no lo
tienen. Las preguntas/respuestas se eligen según slug. Idempotente.
"""
import json
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"

# FAQs por slug de servicio
SERVICE_FAQS = {
    "limpieza-fosas-septicas": [
        ("¿Cada cuánto tiempo se debe limpiar una fosa séptica en Chile?",
         "En general cada 1 a 3 años, dependiendo del número de personas, el tamaño de la fosa y el uso. Una vivienda con 4 personas suele necesitar limpieza cada 18 a 24 meses. Señales como malos olores o lentitud al desaguar indican saturación."),
        ("¿Cuánto cuesta la limpieza de una fosa séptica en Santiago?",
         "El valor referencial parte desde $90.000 para fosas residenciales pequeñas (3-5 m³) y sube a $150.000-$220.000 para fosas mayores o pozos absorbentes. Incluye vaciado con camión limpiafosas, transporte y certificado de disposición final."),
        ("¿Entregan certificado de retiro de lodos?",
         "Sí. Entregamos certificado conforme al D.S. N°4/2009 con folio, patente del camión y planta autorizada de disposición. Es el documento que exige la SEREMI de Salud y que respalda al propietario ante fiscalizaciones."),
        ("¿Atienden parcelas en Chicureo, Pirque o Colina?",
         "Sí. Llegamos a Chicureo, Colina, Lampa, Pirque, Buin, Paine, Talagante y resto de la periferia rural de la RM con camiones propios de alto vacío. Coordinamos horario de acceso y vehículo según el tamaño de la fosa.")
    ],
    "destape-alcantarillado": [
        ("¿Pueden destapar alcantarillado sin romper el piso?",
         "Sí. Usamos sondas eléctricas y hidrojet que destapan desde las cámaras o registros. Solo en casos de raíces avanzadas o tuberías colapsadas se requiere excavación, y siempre se confirma antes con inspección por cámara CCTV."),
        ("¿Cuánto demora un destape de alcantarillado?",
         "Un destape estándar tarda entre 30 y 90 minutos. Casos complejos con raíces o grasa endurecida pueden requerir 2 a 3 horas e hidrojet. Llegamos en promedio en 45 minutos a sectores urbanos de la RM."),
        ("¿Trabajan urgencias 24/7 en Santiago?",
         "Sí. Operamos 24 horas, 7 días, incluyendo fines de semana y festivos. Las urgencias por rebalse, WC tapado o alcantarillado obstruido se priorizan con tiempo de respuesta de 45-90 minutos según comuna."),
        ("¿Emiten boleta y factura?",
         "Sí. Emitimos boleta o factura electrónica con todos los datos del servicio. Tenemos resolución sanitaria al día y trabajamos con condominios, empresas y administradores que requieren respaldo formal.")
    ],
    "destape-wc-y-banos": [
        ("¿Cómo destapar un WC sin romper la cerámica?",
         "Lo correcto es usar una sonda flexible o aspiradora industrial, no objetos rígidos ni químicos abrasivos. Nuestro técnico llega con equipo profesional que destapa desde la taza o desde el registro sin daño a la cerámica ni al sello."),
        ("¿Cuánto cuesta destapar un WC?",
         "Desde $35.000 a $60.000 en sectores urbanos de la RM. El valor depende de la complejidad: si el tapón está en la curva del WC o más profundo en el alcantarillado interno. Llegamos en 45 minutos promedio."),
        ("¿Atienden urgencias de WC desbordado en la noche?",
         "Sí, 24/7. Un WC rebalsado es prioridad alta porque genera daño de aguas residuales. Llegamos en menos de 1 hora a Las Condes, Vitacura, Providencia, Ñuñoa y toda el área urbana de Santiago."),
        ("¿Sirve el destapacañerías de supermercado?",
         "Solo para tapones leves de pelo o jabón. Para tapones de papel, toallitas o sarro no funciona y puede dañar el WC. Si insistes con químicos y luego llamas a un técnico, hay que avisar para usar EPP adicional.")
    ],
    "destape-desagues-cocina-y-grasa": [
        ("¿Por qué se tapa el desagüe de la cocina?",
         "Por acumulación de grasa, restos de comida y jabón en las paredes de la tubería. Con el tiempo se forma una costra dura que reduce el diámetro útil del caño. Lo correcto es prevenir con trampa de grasa y limpieza periódica."),
        ("¿Hidrojet o sonda mecánica para grasa?",
         "Para grasa endurecida el hidrojet (camión alta presión) es lo más efectivo: deshace la costra y deja la cañería como nueva. La sonda mecánica abre paso pero no limpia las paredes; queda igual de propensa a taparse."),
        ("¿Cuánto cuesta destapar el lavaplatos?",
         "Desde $35.000 para tapones leves con sonda y desde $90.000 para hidrojet en cañerías de cocina con grasa endurecida. Locales de comida y restaurantes requieren mantención cada 3-6 meses según volumen."),
        ("¿Atienden restaurantes y locales con factura?",
         "Sí. Trabajamos con restaurantes, casinos, sushi y comida rápida emitiendo factura. Mantención preventiva con hidrojet y limpieza de trampa de grasa según norma chilena DS609 para evitar fiscalizaciones del MOP/SISS.")
    ],
    "destape-edificios-condominios": [
        ("¿Quién paga el destape en un edificio o condominio?",
         "Si el tapón está en la columna principal o en la red común, lo paga la administración con cargo a gastos comunes. Si está en el ramal interno del departamento o casa, lo paga el propietario o arrendatario según el contrato."),
        ("¿Hacen mantención preventiva con factura?",
         "Sí. Ofrecemos contratos anuales de mantención con hidrojet y cámara CCTV en columnas verticales y red horizontal, con factura mensual o por servicio y reportes para el comité de administración."),
        ("¿Cuánto cuesta destapar un edificio?",
         "Depende del piso y la ubicación. Un destape de columna desde el subterráneo parte en $120.000-$250.000. La mantención preventiva anual con hidrojet de columnas se cotiza por número de pisos y sale más económica que las urgencias."),
        ("¿Tienen experiencia con condominios cerrados de Chicureo o La Dehesa?",
         "Sí. Atendemos condominios cerrados con mantención de fosas comunes, hidrojet de redes y limpieza de PTAR si las hay. Coordinamos accesos con conserjería y entregamos certificados al administrador.")
    ],
    "inspeccion-camara-alcantarillado": [
        ("¿Cuándo conviene una inspección con cámara CCTV?",
         "Cuando hay tapones recurrentes en el mismo sector, antes de comprar una propiedad, después de un destape mayor, o cuando se sospechan raíces o roturas. Permite ver el estado interno y evitar excavar a ciegas."),
        ("¿Qué entregan después de la inspección?",
         "Un informe con video, fotos clave y diagnóstico de cada hallazgo (raíces, fisuras, contrapendiente, obstrucciones), incluyendo recomendación técnica. Si aplica, se entregan códigos PACP estandarizados para alcantarillado."),
        ("¿Cuánto cuesta la inspección con cámara?",
         "Desde $80.000 para inspecciones residenciales puntuales. Para edificios o tramos largos parte en $150.000-$300.000 según metros y complejidad. Si se contrata destape o reparación posterior, el costo se descuenta."),
        ("¿Sirve para reclamar a un constructor o a la inmobiliaria?",
         "Sí. El informe con video y códigos PACP es usado como prueba ante constructora o póliza de garantía. Detectamos defectos de instalación, contrapendientes y materiales no conformes a normativa.")
    ],
    "camion-alta-presion-hidrojet": [
        ("¿Qué es el hidrojet y para qué sirve?",
         "Es un camión con bomba de alta presión (hasta 4.000 PSI) que dispara agua a través de boquillas especializadas. Limpia el interior de cañerías, retira grasa, raíces y costra, dejando el caño en condición casi nueva."),
        ("¿Hidrojet o destape mecánico, cuál elegir?",
         "El destape mecánico abre paso rápido pero no limpia. El hidrojet limpia las paredes y previene reincidencias. Para urgencias se usa primero la sonda; para mantención y prevención, el hidrojet es la mejor inversión."),
        ("¿Cuánto cuesta el servicio de hidrojet?",
         "Desde $120.000 para tramos residenciales. Edificios y empresas se cotizan por metros lineales y tipo de obstrucción. Suele incluir inspección con cámara antes y después para verificar resultado."),
        ("¿Daña la cañería el hidrojet?",
         "No, si lo opera un técnico calibrando presión y boquilla según material y diámetro. En PVC y HDPE bien instalados es completamente seguro. En cañerías de cemento muy antiguas se evalúa antes con cámara.")
    ],
    "mantencion-preventiva": [
        ("¿Qué incluye un plan de mantención preventiva?",
         "Limpieza programada con hidrojet, inspección con cámara CCTV anual, monitoreo de trampas de grasa, certificados de retiro de lodos y un técnico asignado. Se evita el 90% de las urgencias y los costos imprevistos."),
        ("¿Cada cuánto se realizan las visitas?",
         "Para edificios y condominios: 2 a 4 visitas al año. Para restaurantes y casinos: cada 3-6 meses. Para parcelas con fosa séptica: 1-2 veces al año. La frecuencia se ajusta según el uso y antecedentes del cliente."),
        ("¿Cuánto cuesta un contrato de mantención?",
         "Depende del tamaño y tipo de instalación. Edificios desde $150.000 mensuales. Restaurantes desde $80.000 trimestrales. Empresas con red industrial se cotizan a medida. Sale más barato que tres urgencias al año."),
        ("¿Emiten factura mensual?",
         "Sí. Trabajamos con factura mensual, OC, y reportes técnicos digitales para administradores y áreas de mantención. Tenemos clientes con contratos vigentes desde 2018.")
    ],
    "contratos-empresas-y-condominios": [
        ("¿Cómo funciona un contrato anual con Destape Rápido?",
         "Se define un calendario de visitas, alcance (hidrojet, cámara, fosa, baños), tarifa fija mensual y tiempo de respuesta para urgencias. Se firma contrato y se entrega un técnico de cuenta dedicado."),
        ("¿Atienden urgencias dentro del contrato?",
         "Sí. Las urgencias están incluidas con tiempo de respuesta SLA de 1 a 2 horas según comuna. Sin costo adicional dentro de las visitas convenidas. Si excede, se cobra a tarifa preferencial de contrato."),
        ("¿Trabajan con OC y facturación a 30 días?",
         "Sí. Trabajamos con OC, plazos de pago a 30/60 días previa evaluación, y subimos las facturas a portales de proveedores. Tenemos clientes empresariales con compras consolidadas mensuales."),
        ("¿Cuál es el cliente típico para contratos?",
         "Edificios y condominios con administración, restaurantes y cadenas, plantas industriales, mall y centros comerciales, hoteles y mineras con campamento. El contrato se ajusta a cada operación.")
    ],
    "banos-quimicos": [
        ("¿Cuántos baños químicos necesito para mi evento?",
         "La regla general es 1 baño cada 50-75 personas para 4 horas. Para eventos de más de 6 horas o con alcohol, súbelo a 1 cada 40 personas. Para obras, 1 baño cada 10 trabajadores con limpieza semanal."),
        ("¿Qué es el líquido azul de los baños químicos?",
         "Es una solución biocida con tinte azul que neutraliza olores, descompone residuos y desinfecta. La fórmula moderna es biodegradable. Permite usar el baño hasta 3-5 días sin malos olores ni proliferación bacteriana."),
        ("¿Cuánto cuesta arrendar un baño químico?",
         "Desde $45.000 por evento de 1 día (instalación + retiro). Mensual para obras desde $90.000 con limpieza semanal incluida. Modelos premium con lavamanos y luz desde $120.000."),
        ("¿Hacen entrega y retiro?",
         "Sí. Coordinamos entrega 24-48h antes del evento u obra, instalación nivelada y retiro al término. Limpieza de servicio incluida según frecuencia contratada.")
    ],
}

def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            }
            for q, a in faqs
        ]
    }

def inject_into_html(text, schema_obj):
    if "FAQPage" in text:
        return text, False
    snippet = (
        '\n    <script type="application/ld+json">\n'
        + json.dumps(schema_obj, ensure_ascii=False, indent=2)
        + '\n    </script>\n'
    )
    idx = text.rfind("</head>")
    if idx < 0:
        return text, False
    return text[:idx] + snippet + text[idx:], True

def main():
    added = 0
    for slug, faqs in SERVICE_FAQS.items():
        f = PUBLIC / "servicios" / f"{slug}.html"
        if not f.exists():
            print(f"!! No existe: {f}")
            continue
        text = f.read_text(encoding="utf-8")
        new_text, changed = inject_into_html(text, faq_schema(faqs))
        if changed:
            f.write_text(new_text, encoding="utf-8")
            added += 1
            print(f"+ FAQPage: {f.relative_to(PUBLIC)}")
        else:
            print(f"= ya tiene FAQ: {f.relative_to(PUBLIC)}")

    print(f"\nTotal FAQ inyectados: {added}")

if __name__ == "__main__":
    main()
