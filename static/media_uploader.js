/**
 * MEDIA UPLOADER — carga de imágenes/videos (drag & drop).
 * Componente genérico: inicializa todos los .media-uploader de la página.
 *
 * Dos modos (definido por data-modo):
 *  - "tabs" (default): pestañas URL / Subir archivo (formulario de carreras).
 *  - "duo": archivo a la izquierda y URL a la derecha (modal de noticias).
 *
 * No toca la lógica de envío del formulario: mantiene los <input type="file">
 * y los <input type="url"> con sus nombres originales para que el backend
 * reciba exactamente lo mismo que antes (archivo tiene prioridad sobre URL).
 */
(function () {
    'use strict';

    var TIPOS_ACEPTADOS = {
        imagen: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
        video: ['video/mp4', 'video/webm', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska', 'video/x-m4v']
    };
    var TEXTO_FORMATO = {
        imagen: 'JPG, PNG, GIF o WEBP',
        video: 'MP4, WEBM, MOV, AVI, MKV o M4V'
    };

    function formatearPeso(bytes) {
        if (!bytes) return '';
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1).replace('.', ',') + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1).replace('.', ',') + ' MB';
    }

    function nombreDeUrl(url) {
        try {
            var p = new URL(url);
            var seg = p.pathname.split('/').filter(Boolean).pop();
            return seg ? decodeURIComponent(seg) : p.hostname;
        } catch (e) {
            return url;
        }
    }

    function iniciar() {
        var uploaders = document.querySelectorAll('.media-uploader');
        if (!uploaders.length) return;

        uploaders.forEach(function (root) {
            var tipo = root.getAttribute('data-tipo') === 'video' ? 'video' : 'imagen';
            var modo = root.getAttribute('data-modo') === 'duo' ? 'duo' : 'tabs';
            var esImagen = tipo === 'imagen';
            var aceptados = TIPOS_ACEPTADOS[tipo];
            var textoFormato = TEXTO_FORMATO[tipo];

            var tabs = root.querySelectorAll('.media-tab');
            var panelUrl = root.querySelector('[data-panel="url"]');
            var panelFile = root.querySelector('[data-panel="file"]');
            var urlInput = root.querySelector('.media-url-input');
            var fileInput = root.querySelector('.media-file-input');
            var dropZone = root.querySelector('.drop-zone');
            var preview = root.querySelector('.media-preview');
            var previewMedia = root.querySelector('.media-preview-media');
            var previewName = root.querySelector('.media-preview-name');
            var previewSize = root.querySelector('.media-preview-size');
            var removeBtn = root.querySelector('.media-preview-remove');
            var errorBox = root.querySelector('.media-error');

            var fuente = 'url';
            var objectUrl = null;

            function limpiarError() {
                errorBox.classList.remove('visible');
                errorBox.textContent = '';
                root.classList.remove('media-has-error');
            }

            function mostrarError(msg) {
                errorBox.textContent = msg;
                errorBox.classList.add('visible');
                root.classList.add('media-has-error');
            }

            function esValido(file) {
                return !!file && aceptados.indexOf(file.type) !== -1;
            }

            // Qué fuente muestra el preview: en "duo" el archivo tiene prioridad.
            function fuenteActiva() {
                if (modo === 'duo') {
                    if (fileInput.files && fileInput.files[0]) return 'file';
                    if (urlInput.value.trim()) return 'url';
                    return null;
                }
                return fuente;
            }

            function setFuente(f) {
                fuente = f;
                tabs.forEach(function (t) {
                    var activo = t.getAttribute('data-tab') === f;
                    t.classList.toggle('active', activo);
                    t.setAttribute('aria-selected', activo ? 'true' : 'false');
                });
                panelUrl.style.display = f === 'url' ? '' : 'none';
                panelFile.style.display = f === 'file' ? '' : 'none';
                limpiarError();
                render();
            }

            function pintarImagen(src) {
                previewMedia.innerHTML = '';
                var img = document.createElement('img');
                img.src = src;
                img.alt = 'Vista previa';
                img.onerror = function () { preview.classList.remove('visible'); };
                previewMedia.appendChild(img);
            }

            function pintarVideo() {
                previewMedia.innerHTML = '<i class="bi bi-film"></i>';
            }

            function render() {
                var activa = fuenteActiva();
                if (!activa) { preview.classList.remove('visible'); return; }

                if (activa === 'url') {
                    var valor = urlInput.value.trim();
                    if (!valor) { preview.classList.remove('visible'); return; }
                    previewName.textContent = nombreDeUrl(valor);
                    previewSize.textContent = '';
                    if (esImagen) pintarImagen(valor); else pintarVideo();
                } else {
                    var file = fileInput.files && fileInput.files[0];
                    if (!file) { preview.classList.remove('visible'); return; }
                    previewName.textContent = file.name;
                    previewSize.textContent = formatearPeso(file.size);
                    if (objectUrl) { URL.revokeObjectURL(objectUrl); objectUrl = null; }
                    if (esImagen) {
                        objectUrl = URL.createObjectURL(file);
                        pintarImagen(objectUrl);
                    } else {
                        pintarVideo();
                    }
                }
                preview.classList.add('visible');
            }

            function limpiarArchivo() {
                fileInput.value = '';
                if (objectUrl) { URL.revokeObjectURL(objectUrl); objectUrl = null; }
            }

            function manejarArchivo(file) {
                limpiarError();
                if (!file) { preview.classList.remove('visible'); return; }
                if (!esValido(file)) {
                    mostrarError('Formato no válido. Usá ' + textoFormato + '.');
                    limpiarArchivo();
                    preview.classList.remove('visible');
                    return;
                }
                render();
            }

            // Pestañas URL / Subir archivo (solo en modo "tabs")
            if (modo === 'tabs') {
                tabs.forEach(function (tab) {
                    tab.addEventListener('click', function () { setFuente(tab.getAttribute('data-tab')); });
                });
            }

            // Vista previa en vivo mientras se escribe la URL
            urlInput.addEventListener('input', function () {
                if (modo === 'tabs' && fuente !== 'url') return;
                render();
            });

            // Selección nativa y archivo recortado con Cropper
            fileInput.addEventListener('change', function () {
                manejarArchivo(fileInput.files && fileInput.files[0]);
            });

            // Click y teclado (accesibilidad) en la zona
            dropZone.addEventListener('click', function () { fileInput.click(); });
            dropZone.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    fileInput.click();
                }
            });

            // Drag & drop
            ['dragenter', 'dragover'].forEach(function (ev) {
                dropZone.addEventListener(ev, function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    dropZone.classList.add('drag-over');
                });
            });
            ['dragleave', 'drop'].forEach(function (ev) {
                dropZone.addEventListener(ev, function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    dropZone.classList.remove('drag-over');
                });
            });
            dropZone.addEventListener('drop', function (e) {
                var file = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
                if (!file) return;
                var dt = new DataTransfer();
                dt.items.add(file);
                fileInput.files = dt.files;
                fileInput.dispatchEvent(new Event('change', { bubbles: true }));
            });

            // Quitar selección
            removeBtn.addEventListener('click', function () {
                if (modo === 'duo') {
                    if (fileInput.files && fileInput.files[0]) {
                        limpiarArchivo();
                    } else {
                        urlInput.value = '';
                    }
                } else if (fuente === 'url') {
                    urlInput.value = '';
                } else {
                    limpiarArchivo();
                }
                limpiarError();
                render();
            });

            // Si el recorte de Cropper reemplaza el archivo, refrescá el preview
            var cropModal = document.getElementById('cropModal');
            if (cropModal) {
                cropModal.addEventListener('hidden.bs.modal', function () { render(); });
            }

            // Modales: re-render al abrir y resetear al cerrar
            var modal = root.closest('.modal');
            if (modal) {
                modal.addEventListener('show.bs.modal', function () {
                    if (modo === 'tabs') setFuente(urlInput.value.trim() ? 'url' : 'file');
                    else render();
                });
                modal.addEventListener('hidden.bs.modal', function () {
                    limpiarArchivo();
                    if (modo === 'duo') urlInput.value = '';
                    limpiarError();
                    render();
                });
            }

            // Estado inicial
            if (modo === 'tabs') setFuente(urlInput.value.trim() ? 'url' : 'file');
            else render();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', iniciar);
    } else {
        iniciar();
    }
})();