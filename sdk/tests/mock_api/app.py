# AtriumDB is a timeseries database software designed to best handle the unique features and
# challenges that arise from clinical waveform data.
#     Copyright (C) 2023  The Hospital for Sick Children
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from fastapi import FastAPI

from tests.mock_api.devices_endpoints import devices_router
from tests.mock_api.measures_endpoints import measures_router
from tests.mock_api.sdk_endpoints import sdk_router

app = FastAPI()
app.include_router(sdk_router, prefix="/sdk")
app.include_router(measures_router, prefix="/measures")
app.include_router(devices_router, prefix="/devices")
