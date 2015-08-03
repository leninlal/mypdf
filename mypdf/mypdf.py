"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment


class MyPdfXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    icon_class = "other"

    display_name = String(display_name="Display Name",
        default="PDF",
        scope=Scope.settings,
        help="This name appears in the horizontal navigation at the top of the page.")

    url = String(display_name="PDF URL",
        default="http://www.tutorialspoint.com/python/python_tutorial.pdf",
        scope=Scope.content,
        help="The URL for your PDF.")
    
    allow_download = Boolean(display_name="PDF Download Allowed",
        default=True,
        scope=Scope.content,
        help="Display a download button for this PDF.")

    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)
        return unicode(resource_content)

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))

    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """
        
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download
        }
        html = self.render_template('static/html/mypdf_view.html', context)
        
        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/mypdf.css"))
        frag.add_javascript(self.load_resource("static/js/mypdf_view.js"))
        frag.initialize_js('pdfXBlockInitView')
        return frag

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download
        }
        html = self.render_template('static/html/mypdf_edit.html', context)
        
        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/mypdf_edit.js"))
        frag.initialize_js('pdfXBlockInitEdit')
        return frag

    @XBlock.json_handler
    def save_pdf(self, data, suffix=''):
        """
        The saving handler.
        """
        self.display_name = data['display_name']
        self.url = data['url']
        self.allow_download = True if data['allow_download'] == "True" else False # Str to Bool translation
        
        return {
            'result': 'success',
        }
