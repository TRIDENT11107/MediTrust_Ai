import { useEffect, useRef, useState } from 'react';

const MAX_SIZE_BYTES = 10 * 1024 * 1024;
const ALLOWED_TYPES = ['image/png', 'image/jpeg', 'application/pdf', 'image/jpg'];
const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');
const API_KEY = import.meta.env.VITE_API_KEY || '';
const SAMPLE_OPTIONS = [
  { label: 'Sample: X_019.jpeg', value: '/static/uploads/X_019.jpeg', policy: 'default' },
  { label: 'Sample: X_081.jpeg', value: '/static/uploads/X_081.jpeg', policy: 'default' },
  { label: 'Sample PDF (simulated)', value: 'pdf-sample', policy: 'pdf_sample' },
];

function buildUrl(path) {
  if (!path) return '';
  if (/^https?:\/\//i.test(path)) return path;
  return API_BASE ? `${API_BASE}${path.startsWith('/') ? path : `/${path}`}` : path;
}

export default function Dropzone() {
  const [file, setFile] = useState(null);
  const [selectedSample, setSelectedSample] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [labelText, setLabelText] = useState('Drag and drop files here');
  const [previewUrl, setPreviewUrl] = useState('');
  const inputRef = useRef(null);
  const dropRef = useRef(null);
  const labelTimerRef = useRef(null);

  useEffect(() => {
    const dz = dropRef.current;
    if (!dz) return undefined;

    function preventDefaults(event) {
      event.preventDefault();
      event.stopPropagation();
    }

    const addActive = () => dz.classList.add('active');
    const removeActive = () => dz.classList.remove('active');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach((eventName) => {
      dz.addEventListener(eventName, preventDefaults);
    });
    ['dragenter', 'dragover'].forEach((eventName) => {
      dz.addEventListener(eventName, addActive);
    });
    ['dragleave', 'drop'].forEach((eventName) => {
      dz.addEventListener(eventName, removeActive);
    });

    return () => {
      ['dragenter', 'dragover', 'dragleave', 'drop'].forEach((eventName) => {
        dz.removeEventListener(eventName, preventDefaults);
      });
      ['dragenter', 'dragover'].forEach((eventName) => {
        dz.removeEventListener(eventName, addActive);
      });
      ['dragleave', 'drop'].forEach((eventName) => {
        dz.removeEventListener(eventName, removeActive);
      });
    };
  }, []);

  useEffect(() => {
    if (!file || file.type === 'application/pdf') {
      setPreviewUrl('');
      return undefined;
    }

    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);

    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [file]);

  useEffect(() => () => {
    if (labelTimerRef.current) {
      window.clearTimeout(labelTimerRef.current);
    }
  }, []);

  function showMessage(message) {
    setLabelText(message);
    if (labelTimerRef.current) {
      window.clearTimeout(labelTimerRef.current);
    }
    labelTimerRef.current = window.setTimeout(() => {
      setLabelText('Drag and drop files here');
    }, 2500);
  }

  function validateFile(nextFile) {
    if (!nextFile) {
      return 'Choose a file first';
    }
    if (!ALLOWED_TYPES.includes(nextFile.type)) {
      return `Unsupported file type: ${nextFile.type || 'unknown'}`;
    }
    if (nextFile.size > MAX_SIZE_BYTES) {
      return `File is larger than 10MB: ${nextFile.name}`;
    }
    return '';
  }

  function setDocument(nextFile) {
    const validationError = validateFile(nextFile);
    if (validationError) {
      setError(validationError);
      setResult(null);
      showMessage(validationError);
      return;
    }

    setFile(nextFile);
    setSelectedSample('');
    setResult(null);
    setError('');
    showMessage(`Ready: ${nextFile.name}`);
  }

  function handleDrop(event) {
    const [droppedFile] = Array.from(event.dataTransfer.files || []);
    setDocument(droppedFile);
  }

  function handlePick(event) {
    const [pickedFile] = Array.from(event.target.files || []);
    setDocument(pickedFile);
    event.target.value = '';
  }

  function handleDropzoneClick(event) {
    if (event.target.closest('select, button, input, #results-panel')) return;
    inputRef.current?.click();
  }

  function handleDropzoneKeydown(event) {
    if (event.target.closest('select, button, input, #results-panel')) return;
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      inputRef.current?.click();
    }
  }

  async function ping() {
    const response = await fetch(buildUrl('/api/health'));
    if (!response.ok) {
      const body = await response.text().catch(() => '');
      throw new Error(
        body || `Backend unreachable. Start the API service and confirm ${buildUrl('/api/health')} responds.`
      );
    }
  }

  async function processBlob(blob, filename, policy = 'default') {
    await ping();

    const formData = new FormData();
    formData.append('file', blob, filename);

    const headers = API_KEY ? { 'x-api-key': API_KEY } : undefined;
    const query = policy && policy !== 'default' ? `?policy=${encodeURIComponent(policy)}` : '';
    const response = await fetch(buildUrl(`/api/process${query}`), {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      const body = await response.text().catch(() => '');
      throw new Error(body || `Processing failed with status ${response.status}`);
    }

    return response.json();
  }

  async function handleProcess() {
    if (!file && !selectedSample) {
      const message = 'Choose a file or sample first';
      setError(message);
      showMessage(message);
      return;
    }

    setIsProcessing(true);
    setError('');

    try {
      let nextResult;

      if (file) {
        nextResult = await processBlob(file, file.name);
      } else if (selectedSample === 'pdf-sample') {
        const blob = new Blob(['Sample PDF upload'], { type: 'application/pdf' });
        nextResult = await processBlob(blob, 'sample.pdf', 'pdf_sample');
      } else {
        const sampleResponse = await fetch(buildUrl(selectedSample));
        if (!sampleResponse.ok) {
          throw new Error(`Could not load sample (${sampleResponse.status})`);
        }
        const blob = await sampleResponse.blob();
        const filename = selectedSample.split('/').pop() || 'sample';
        nextResult = await processBlob(blob, filename);
      }

      setResult(nextResult);
      showMessage(`Processed: ${nextResult.filename}`);
    } catch (nextError) {
      const message = normalizeError(nextError);
      setResult(null);
      setError(message);
      showMessage(message);
    } finally {
      setIsProcessing(false);
    }
  }

  function clearAll() {
    setFile(null);
    setSelectedSample('');
    setResult(null);
    setError('');
    setPreviewUrl('');
    showMessage('Cleared current document');
  }

  const redactedUrl = result?.output_url ? buildUrl(result.output_url) : '';
  const piiCount = Array.isArray(result?.pii_detected) ? result.pii_detected.length : 0;
  const boxCount = Array.isArray(result?.boxes_applied) ? result.boxes_applied.length : 0;

  return (
    <div className="relative" data-aos="fade-left">
      <div
        ref={dropRef}
        className="dropzone relative bg-gray-50 rounded-lg border-2 border-dashed p-12 text-center focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        tabIndex={0}
        onDrop={handleDrop}
        onClick={handleDropzoneClick}
        onKeyDown={handleDropzoneKeydown}
      >
        <i data-feather="upload" className="mx-auto h-12 w-12 text-gray-400"></i>
        <h3 className="mt-2 text-sm font-medium text-gray-900">
          <label htmlFor="file-upload" className="relative cursor-pointer">
            <span id="dropzone-label">{labelText}</span>
            <input
              id="file-upload"
              name="file-upload"
              ref={inputRef}
              type="file"
              className="sr-only"
              accept="image/*,.pdf"
              onChange={handlePick}
            />
          </label>
        </h3>
        <p className="mt-1 text-xs text-gray-500">PDF, JPG, PNG up to 10MB</p>

        <div className="mt-6 flex flex-wrap items-center justify-center gap-2">
          <select
            id="sample-select"
            className="rounded-md border-gray-200 text-sm p-2"
            value={selectedSample}
            onChange={(event) => {
              setSelectedSample(event.target.value);
              setFile(null);
              setResult(null);
              setError('');
            }}
          >
            <option value="">Choose a sample</option>
            {SAMPLE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <button
            id="process-document"
            className="bg-indigo-600 text-white px-3 py-2 rounded-md text-sm disabled:opacity-60"
            disabled={isProcessing}
            onClick={handleProcess}
          >
            {isProcessing ? 'Processing...' : 'Process document'}
          </button>
          <button
            id="clear-files"
            className="bg-gray-200 text-gray-700 px-3 py-2 rounded-md text-sm disabled:opacity-60"
            disabled={isProcessing}
            onClick={clearAll}
          >
            Clear
          </button>
        </div>

        <div id="results-panel" className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4 text-left">
          {file && (
            <div className="bg-white rounded-md p-3 shadow flex flex-col gap-3">
              <p className="text-sm font-semibold text-gray-900">Selected file</p>
              {previewUrl ? (
                <img className="w-full rounded-md object-cover max-h-48" alt={file.name} src={previewUrl} />
              ) : (
                <div className="w-full p-6 border border-dashed rounded-md text-center text-sm text-gray-600">
                  {file.name}
                </div>
              )}
              <div className="text-sm text-gray-700 font-medium">{file.name}</div>
              <div className="text-xs text-gray-500">{(file.size / 1024).toFixed(0)} KB</div>
            </div>
          )}

          {!file && selectedSample && (
            <div className="bg-white rounded-md p-3 shadow flex flex-col gap-3">
              <p className="text-sm font-semibold text-gray-900">Selected sample</p>
              <div className="w-full p-6 border border-dashed rounded-md text-center text-sm text-gray-600">
                {SAMPLE_OPTIONS.find((option) => option.value === selectedSample)?.label || selectedSample}
              </div>
            </div>
          )}

          {result && (
            <div className="bg-white rounded-md p-3 shadow flex flex-col gap-3">
              <p className="text-sm font-semibold text-gray-900">Processed output</p>
              {redactedUrl && !result.is_pdf ? (
                <img className="w-full rounded-md object-cover max-h-48" alt={`${result.filename} redacted`} src={redactedUrl} />
              ) : (
                <a className="text-sm text-indigo-600 underline break-all" href={redactedUrl} target="_blank" rel="noreferrer">
                  Open output
                </a>
              )}
              <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                <div>
                  <div className="font-semibold text-gray-900">PII matches</div>
                  <div>{piiCount}</div>
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Boxes applied</div>
                  <div>{boxCount}</div>
                </div>
                <div>
                  <div className="font-semibold text-gray-900">OCR chars</div>
                  <div>{result.ocr_chars || 0}</div>
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Policy</div>
                  <div>{result.policy}</div>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="sm:col-span-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          {result && (
            <div className="sm:col-span-2 rounded-md bg-gray-900 p-3 text-xs text-gray-100 overflow-auto">
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
          )}
        </div>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-4">
        <div className="bg-indigo-100 rounded-md p-3 text-center">
          <p className="text-sm font-medium text-indigo-700">Prescriptions</p>
        </div>
        <div className="bg-indigo-100 rounded-md p-3 text-center">
          <p className="text-sm font-medium text-indigo-700">Consent Forms</p>
        </div>
        <div className="bg-indigo-100 rounded-md p-3 text-center">
          <p className="text-sm font-medium text-indigo-700">Lab Reports</p>
        </div>
      </div>
    </div>
  );
}

function normalizeError(error) {
  const message = error?.message || String(error);

  if (message === 'Failed to fetch') {
    const target = API_BASE || 'the current app origin';
    return `Backend unreachable. Start the API service and confirm ${target}/api/health responds.`;
  }

  return message;
}
