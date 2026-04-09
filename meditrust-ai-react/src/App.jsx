import Dropzone from './components/Dropzone'

export default function App(){
  return (
    <div className="font-sans antialiased text-gray-800">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <i data-feather="shield" className="h-8 w-8 text-indigo-600"></i>
                <span className="ml-2 text-xl font-bold text-gray-900">MediTrust AI</span>
              </div>
            </div>
            <div className="hidden md:ml-6 md:flex md:items-center md:space-x-8">
              <a href="#" className="text-indigo-600 border-b-2 border-indigo-500 px-3 py-2 text-sm font-medium">Home</a>
              <a href="#" className="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium">Features</a>
              <a href="#" className="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium">Documentation</a>
              <a href="#" className="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium">Pricing</a>
              <button className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Try Demo</button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <div className="gradient-bg text-white">
        <div className="max-w-7xl mx-auto py-16 px-4 sm:py-24 sm:px-6 lg:px-8">
          <div className="text-center" data-aos="fade-up">
            <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl">Protect Patient Privacy Automatically</h1>
            <p className="mt-6 max-w-3xl mx-auto text-xl text-indigo-100">AI-powered PII detection and redaction for healthcare documents while preserving clinical content integrity.</p>
            <div className="mt-10 flex justify-center space-x-4">
              <a href="#" className="bg-white text-indigo-600 px-8 py-3 border border-transparent rounded-md text-base font-medium hover:bg-indigo-50 md:py-4 md:text-lg md:px-10">Get Started</a>
              <a href="#" className="bg-indigo-700 bg-opacity-60 px-8 py-3 border border-transparent rounded-md text-base font-medium text-white hover:bg-opacity-70 md:py-4 md:text-lg md:px-10">Live Demo</a>
            </div>
          </div>
        </div>
      </div>

      {/* Document Types Section */}
      <div className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12" data-aos="fade-up">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">Supported Healthcare Documents</h2>
            <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">We automatically detect and protect PII across all major healthcare document types.</p>
          </div>

          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <div className="document-card bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300" data-aos="fade-up" data-aos-delay="100">
              <div className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                    <i data-feather="file-text" className="h-6 w-6 text-indigo-600"></i>
                  </div>
                  <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Prescriptions</h3></div>
                </div>
                <p className="mt-4 text-gray-500">Redact patient identifiers while preserving medication details and doctor signatures.</p>
              </div>
            </div>

            <div className="document-card bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300" data-aos="fade-up" data-aos-delay="200">
              <div className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                    <i data-feather="edit" className="h-6 w-6 text-indigo-600"></i>
                  </div>
                  <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Consent Forms</h3></div>
                </div>
                <p className="mt-4 text-gray-500">Protect patient signatures while maintaining procedure consent details.</p>
              </div>
            </div>

            <div className="document-card bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300" data-aos="fade-up" data-aos-delay="300">
              <div className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                    <i data-feather="clipboard" className="h-6 w-6 text-indigo-600"></i>
                  </div>
                  <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Discharge Summaries</h3></div>
                </div>
                <p className="mt-4 text-gray-500">Redact PII while preserving critical clinical information for continuity of care.</p>
              </div>
            </div>

            <div className="document-card bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300" data-aos="fade-up" data-aos-delay="400">
              <div className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                    <i data-feather="mail" className="h-6 w-6 text-indigo-600"></i>
                  </div>
                  <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Referral Letters</h3></div>
                </div>
                <p className="mt-4 text-gray-500">Protect patient details while maintaining referral context and doctor information.</p>
              </div>
            </div>

            <div className="document-card bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300" data-aos="fade-up" data-aos-delay="500">
              <div className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                    <i data-feather="dollar-sign" className="h-6 w-6 text-indigo-600"></i>
                  </div>
                  <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Insurance Claims</h3></div>
                </div>
                <p className="mt-4 text-gray-500">Secure sensitive information while preserving claim details for processing.</p>
              </div>
            </div>

            <div className="document-card bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300" data-aos="fade-up" data-aos-delay="600">
              <div className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                    <i data-feather="activity" className="h-6 w-6 text-indigo-600"></i>
                  </div>
                  <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Lab Reports</h3></div>
                </div>
                <p className="mt-4 text-gray-500">Protect patient identifiers while maintaining test results and clinical findings.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* PII Detection Section */}
      <div className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center" data-aos="fade-up">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">What We Detect and Protect</h2>
            <p className="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">Our AI models identify and redact various types of sensitive information.</p>
          </div>

          <div className="mt-16">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              <div className="bg-white rounded-lg shadow-md overflow-hidden" data-aos="fade-up" data-aos-delay="100">
                <div className="p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                      <i data-feather="edit-3" className="h-6 w-6 text-indigo-600"></i>
                    </div>
                    <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Handwritten Signatures</h3></div>
                  </div>
                  <p className="mt-4 text-gray-500">Distinguishes between patient and doctor signatures with role-aware redaction.</p>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md overflow-hidden" data-aos="fade-up" data-aos-delay="200">
                <div className="p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                      <i data-feather="user" className="h-6 w-6 text-indigo-600"></i>
                    </div>
                    <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Patient Identifiers</h3></div>
                  </div>
                  <p className="mt-4 text-gray-500">Names, DOBs, MRNs, phone numbers and other direct identifiers.</p>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md overflow-hidden" data-aos="fade-up" data-aos-delay="300">
                <div className="p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                      <i data-feather="credit-card" className="h-6 w-6 text-indigo-600"></i>
                    </div>
                    <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Government IDs</h3></div>
                  </div>
                  <p className="mt-4 text-gray-500">Aadhaar, SSN, and other national identification numbers.</p>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md overflow-hidden" data-aos="fade-up" data-aos-delay="400">
                <div className="p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                      <i data-feather="image" className="h-6 w-6 text-indigo-600"></i>
                    </div>
                    <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Embedded Photos</h3></div>
                  </div>
                  <p className="mt-4 text-gray-500">Detects and redacts faces in embedded patient photos.</p>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md overflow-hidden" data-aos="fade-up" data-aos-delay="500">
                <div className="p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                      <i data-feather="archive" className="h-6 w-6 text-indigo-600"></i>
                    </div>
                    <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Hospital Stamps</h3></div>
                  </div>
                  <p className="mt-4 text-gray-500">Identifies and redacts institutional stamps and seals containing PII.</p>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md overflow-hidden" data-aos="fade-up" data-aos-delay="600">
                <div className="p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md">
                      <i data-feather="maximize-2" className="h-6 w-6 text-indigo-600"></i>
                    </div>
                    <div className="ml-4"><h3 className="text-lg font-medium text-gray-900">Barcodes/QR Codes</h3></div>
                  </div>
                  <p className="mt-4 text-gray-500">Detects and redacts machine-readable identifiers.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Upload Section with Dropzone */}
      <div className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-2 lg:gap-8 lg:items-center">
            <div className="mb-8 lg:mb-0" data-aos="fade-right">
              <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">Simple Drag-and-Drop Interface</h2>
              <p className="mt-4 text-lg text-gray-500">Upload your healthcare documents and let our AI automatically detect and redact sensitive information.</p>
              <div className="mt-8">
                <div className="inline-flex rounded-md shadow">
                  <a href="#" className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">Try Demo<i data-feather="arrow-right" className="ml-2 w-4 h-4"></i></a>
                </div>
              </div>
            </div>
            <div className="relative" data-aos="fade-left">
              <Dropzone />
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12" data-aos="fade-up">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">Why Choose MediTrust AI</h2>
            <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">Our unique approach to healthcare document privacy protection.</p>
          </div>

          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            <div className="bg-white rounded-lg shadow-md overflow-hidden p-6" data-aos="fade-up" data-aos-delay="100">
              <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md inline-flex"><i data-feather="users" className="h-6 w-6 text-indigo-600"></i></div>
              <h3 className="mt-4 text-lg font-medium text-gray-900">Role-Aware Processing</h3>
              <p className="mt-2 text-gray-500">Distinguishes between patient and doctor signatures for context-appropriate redaction.</p>
            </div>

            <div className="bg-white rounded-lg shadow-md overflow-hidden p-6" data-aos="fade-up" data-aos-delay="200">
              <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md inline-flex"><i data-feather="shield" className="h-6 w-6 text-indigo-600"></i></div>
              <h3 className="mt-4 text-lg font-medium text-gray-900">Privacy-First Defaults</h3>
              <p className="mt-2 text-gray-500">Automatic redaction of patient signatures with configurable policies.</p>
            </div>

            <div className="bg-white rounded-lg shadow-md overflow-hidden p-6" data-aos="fade-up" data-aos-delay="300">
              <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md inline-flex"><i data-feather="bar-chart-2" className="h-6 w-6 text-indigo-600"></i></div>
              <h3 className="mt-4 text-lg font-medium text-gray-900">MediTrust Score</h3>
              <p className="mt-2 text-gray-500">Per-document confidence score for PII detection accuracy.</p>
            </div>

            <div className="bg-white rounded-lg shadow-md overflow-hidden p-6" data-aos="fade-up" data-aos-delay="400">
              <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-md inline-flex"><i data-feather="server" className="h-6 w-6 text-indigo-600"></i></div>
              <h3 className="mt-4 text-lg font-medium text-gray-900">On-Premise Ready</h3>
              <p className="mt-2 text-gray-500">Runs offline with no third-party data egress for maximum security.</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="gradient-bg">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
          <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl" data-aos="fade-right"><span className="block">Ready to protect patient privacy?</span><span className="block text-indigo-200">Start your free trial today.</span></h2>
          <div className="mt-8 flex lg:mt-0 lg:flex-shrink-0" data-aos="fade-left">
            <div className="inline-flex rounded-md shadow"><a href="#" className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50">Get started</a></div>
            <div className="ml-3 inline-flex rounded-md shadow"><a href="#" className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 bg-opacity-60 hover:bg-opacity-70">Live demo</a></div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Product</h3>
              <ul className="mt-4 space-y-4"><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">Features</a></li><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">Pricing</a></li><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">API</a></li></ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Resources</h3>
              <ul className="mt-4 space-y-4"><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">Documentation</a></li><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">Guides</a></li><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">Blog</a></li></ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Company</h3>
              <ul className="mt-4 space-y-4"><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">About</a></li><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">Careers</a></li><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">Contact</a></li></ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Legal</h3>
              <ul className="mt-4 space-y-4"><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">Privacy</a></li><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">Terms</a></li><li><a href="#" className="text-base text-gray-500 hover:text-gray-900">Compliance</a></li></ul>
            </div>
          </div>
          <div className="mt-12 border-t border-gray-200 pt-8 flex items-center justify-between">
            <p className="text-base text-gray-400">&copy; 2023 MediTrust AI. All rights reserved.</p>
            <div className="flex space-x-6"><a href="#" className="text-gray-400 hover:text-gray-500"><i data-feather="twitter" className="h-6 w-6"></i></a><a href="#" className="text-gray-400 hover:text-gray-500"><i data-feather="linkedin" className="h-6 w-6"></i></a><a href="#" className="text-gray-400 hover:text-gray-500"><i data-feather="github" className="h-6 w-6"></i></a></div>
          </div>
        </div>
      </footer>
    </div>
  )
}
