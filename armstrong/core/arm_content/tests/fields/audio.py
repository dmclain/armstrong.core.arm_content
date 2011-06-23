# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from ..arm_content_support.models import AudioModel
from ..arm_content_support.forms import AudioModelForm
from ..arm_content_support.models import SimpleProfile

from .._utils import *
from ...fields import AudioField
from ...fields.widgets.audio import AudioFileWidget 

class AudioFieldMetadataTestCase(TestCase):
    def setUp(self):
        if type(self) is AudioFieldMetadataTestCase:
            return self.skipTest('parrent class')
        self.audiofile = load_audio_file(self.filename)

    def test_audiofield_default_widget(self):
        """
        test that the correct widget is displayed in 
        a model form 
        """
        form=AudioModelForm()
        self.assertTrue(type(form.fields['audio_file'].widget) is AudioFileWidget)
        form2=AudioModelForm(initial={"audio_file":self.audiofile.audio_file})
        self.assertTrue(self.audiofile.audio_file.url in form2.as_ul()  )

    def test_audiofield_filetype(self):
        """
        test that the file type returned by the file field is correct
        """
        self.assertEqual(self.audiofile.audio_file.filetype, self.filetype)
        
    def test_audiofield_metadata(self):
        """
        confirm that the extracted metadata matches the expected values 
        """
        for key in self.audio_metadata.keys():
            self.assertEqual(self.audio_metadata[key], self.audiofile.audio_file.metadata[key])


class MutagenMp3Test(AudioFieldMetadataTestCase):
    """
    tests the audio fields support for mp3's
    """
    filename='test.mp3'
    filetype='mp3'
    playtime='4'
    audio_metadata={'album': [u'Quod Libet Test Data'],
                    'title': [u'Silence'], 
                    'artist': [u'piman'],
                    'genre': [u'Darkwave'], 
                    'date': [u'2004'],
                    'tracknumber': [u'2']
                    }

class MutagenOggTest(AudioFieldMetadataTestCase):
    """
    tests the audio fields support for ogg's
    """
    filename='test.ogg'
    filetype='ogg'
    playtime='264'
    audio_metadata={'album': [u'Favorite Things'],
                    'title': [u'Hydrate - Kenny Beltrey'], 
                    'artist': [u'Kenny Beltrey'],
                    'date': [u'2002'],
                    'tracknumber': [u'2'],
                    'comment': [u'http://www.kahvi.org'],
                    }

class Id3readerTest(Mp3Test):
    """
    test id3reader by temporarrily overriding the settings 
    """
    def setUp(self):
        self.org_backend=settings.ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND
        settings.ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND = 'armstrong.core.arm_content.audio.backends.MutagenBackend'
        super(self, Id3readerTest).setUp(self)

    def tearDown(self):
        settings.ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND = self.org_backend
