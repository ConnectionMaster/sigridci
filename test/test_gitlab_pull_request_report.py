# Copyright Software Improvement Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
from tempfile import mkdtemp
from unittest import TestCase, mock

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.gitlab_pull_request_report import GitLabPullRequestReport
from sigridci.sigridci.reports.maintainability_markdown_report import MaintainabilityMarkdownReport
from sigridci.sigridci.reports.security_markdown_report import SecurityMarkdownReport
from sigridci.sigridci.upload_log import UploadLog


MOCK_GITLAB_ENV = {
    "CI_API_V4_URL" : "https://example.com",
    "CI_MERGE_REQUEST_PROJECT_ID" : "1234",
    "CI_MERGE_REQUEST_IID" : "5678"
}


class GitLabPullRequestReportTest(TestCase):

    def setUp(self):
        UploadLog.clear()
        self.tempDir = mkdtemp()
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, targetRating=3.5, outputDir=self.tempDir)

        self.feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
            "refactoringCandidates": []
        }

    @mock.patch.dict(os.environ, MOCK_GITLAB_ENV)
    def testPostNewComment(self):
        gitlab = MockGitLab(MaintainabilityMarkdownReport())
        gitlab.generate("1234", self.feedback, self.options)

        self.assertEqual(["Published Maintainability feedback to GitLab"], UploadLog.history)
        self.assertEqual(["POST https://example.com/projects/1234/merge_requests/5678/notes"], gitlab.called)

    @mock.patch.dict(os.environ, MOCK_GITLAB_ENV)
    def testUpdateExistingComment(self):
        gitlab = MockGitLab(MaintainabilityMarkdownReport())
        gitlab.generate("1234", self.feedback, self.options)
        gitlab.generate("1234", self.feedback, self.options)

        expectedLog = [
            "Published Maintainability feedback to GitLab",
            "Updated existing GitLab Maintainability feedback"
        ]

        expectedCalls = [
            "POST https://example.com/projects/1234/merge_requests/5678/notes",
            "PUT https://example.com/projects/1234/merge_requests/5678/notes/1"
        ]

        self.assertEqual(expectedLog, UploadLog.history)
        self.assertEqual(expectedCalls, gitlab.called)

    @mock.patch.dict(os.environ, MOCK_GITLAB_ENV)
    def testDoNotUpdateDifferentTypeOfFeedback(self):
        gitlab = MockGitLab(MaintainabilityMarkdownReport())
        gitlab.generate("1234", self.feedback, self.options)
        gitlab.generate("1234", self.feedback, self.options)

        other = MockGitLab(SecurityMarkdownReport())
        other.generate("1234", {"runs" : []}, self.options)
        other.generate("1234", {"runs" : []}, self.options)

        expectedLog = [
            "Published Maintainability feedback to GitLab",
            "Updated existing GitLab Maintainability feedback",
            "Published Security feedback to GitLab",
            "Updated existing GitLab Security feedback"
        ]

        self.assertEqual(expectedLog, UploadLog.history)


class MockGitLab(GitLabPullRequestReport):

    def __init__(self, markdownReport):
        super().__init__(markdownReport)
        self.called = []
        self.comments = []

    def callAPI(self, method, url, body):
        self.called.append(f"{method} {url}")
        if method == "POST":
            self.comments.append(json.loads(body) | {"id" : len(self.comments) + 1})
        return self

    def isWithinGitLabMergeRequestPipeline(self, options):
        return True

    def findExistingCommentId(self):
        return next((comment["id"] for comment in self.comments if self.isExistingComment(comment)), None)

    def read(self):
        return "test"
