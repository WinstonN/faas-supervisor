# Copyright (C) GRyCAP - I3M - UPV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from botocore.exceptions import ClientError
import functools
import sys

def exception(logger):
    '''
    A decorator that wraps the passed in function and logs exceptions
    @param logger: The logging object
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ClientError as ce:
                print("There was an exception in {0}".format(func.__name__))
                print(ce.response['Error']['Message'])
                logger.exception(ce)
                sys.exit(1)
            except BaseError as se:
                print(se.args[0])
                logger.exception(se)
                # Finish the execution if it's an error
                if 'Error' in se.__class__.__name__:
                    sys.exit(1)
            except Exception as ex:
                print("There was an unmanaged exception in {0}".format(func.__name__))
                logger.exception(ex)
                sys.exit(1)
        return wrapper
    return decorator

class BaseError(Exception):
    """
    The base exception class for exceptions.

    :ivar msg: The descriptive message associated with the error.
    """
    fmt = 'An unspecified error occurred'

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs

################################################
##             GENERAL EXCEPTIONS             ##
################################################
class InvalidPlatformError(BaseError):
    """
    The binary is not launched on a Linux platform

    """
    fmt = "This binary only works on a Linux Platform.\nTry executing the Python version."
    