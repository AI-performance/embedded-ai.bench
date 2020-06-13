// Tencent is pleased to support the open source community by making TNN available.
//
// Copyright (C) 2020 THL A29 Limited, a Tencent company. All rights reserved.
//
// Licensed under the BSD 3-Clause License (the "License"); you may not use this file except
// in compliance with the License. You may obtain a copy of the License at
//
// https://opensource.org/licenses/BSD-3-Clause
//
// Unless required by applicable law or agreed to in writing, software distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.

#include "tnn/core/tnn_impl_default.h"

#include "tnn/interpreter/default_model_interpreter.h"

namespace TNN_NS {

TNNImplFactoryRegister<TNNImplFactory<TNNImplDefault>> g_tnn_impl_default_factory_register(MODEL_TYPE_TNN);

TNNImplFactoryRegister<TNNImplFactory<TNNImplDefault>> g_tnn_impl_ncnn_factory_register(MODEL_TYPE_NCNN);

TNNImplDefault::TNNImplDefault() {}

TNNImplDefault::~TNNImplDefault() {}

Status TNNImplDefault::Init(ModelConfig& config) {
    auto status = TNNImpl::Init(config);
    if (status != TNN_OK) {
        return status;
    }

    auto interpreter = CreateModelInterpreter(config.model_type);
    if (!interpreter) {
        return Status(TNNERR_NET_ERR, "interpreter is nil");
    }
    interpreter_ = std::shared_ptr<AbstractModelInterpreter>(interpreter);
    return interpreter_->Interpret(config.params);
}

Status TNNImplDefault::DeInit() {
    interpreter_ = nullptr;
    return TNN_OK;
}

Status TNNImplDefault::AddOutput(const std::string& layer_name, int output_index) {
    if (!interpreter_) {
        return Status(TNNERR_NET_ERR, "interpreter is nil");
    }

    auto default_interpreter = dynamic_cast<DefaultModelInterpreter*>(interpreter_.get());
    CHECK_PARAM_NULL(default_interpreter);

    default_interpreter->GetNetStructure()->outputs.insert(layer_name);
    return TNN_OK;
}

std::shared_ptr<Instance> TNNImplDefault::CreateInst(NetworkConfig& net_config, Status& status,
                                                     InputShapesMap inputs_shape) {
    if (!interpreter_) {
        status = Status(TNNERR_NET_ERR, "interpreter is nil");
        return nullptr;
    }

    auto instance = std::make_shared<Instance>(net_config, model_config_);
    status        = instance->Init(interpreter_, inputs_shape);

    if (status != TNN_OK) {
        return nullptr;
    }
    return instance;
}

}  // namespace TNN_NS
