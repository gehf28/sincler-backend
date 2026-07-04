from sqlalchemy import text
from .history_service import engine # Reutilizamos tu motor de conexión existente

def registrar_evento_o_lead(tipo: str, seccion: str, nombre: str = None, correo: str = None):
    """Guarda una interacción o un registro de correo en la tabla unificada."""
    try:
        with engine.begin() as conn:
            query = text("""
                INSERT INTO registro_leads_interacciones (tipo, seccion, nombre, correo)
                VALUES (:tipo, :seccion, :nombre, :correo);
            """)
            conn.execute(query, {
                "tipo": tipo, 
                "seccion": seccion, 
                "nombre": nombre, 
                "correo": correo
            })
            print(f"✅ [Supabase] Registro exitoso: {tipo}")
    except Exception as e:
        print(f"❌ Error al registrar en Supabase: {e}")